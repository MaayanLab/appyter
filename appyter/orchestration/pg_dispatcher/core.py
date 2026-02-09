import asyncio
import datetime
import logging
import json
import asyncpg
from aiohttp import web
logger = logging.getLogger(__name__)

async def create_pool(DATABASE_URL):
  pool = await asyncpg.create_pool(
      DATABASE_URL,
      min_size=1,
      max_size=10,
      command_timeout=10,
  )
  try:
    async with pool.acquire() as conn:
      await conn.execute(
        """
        CREATE TABLE job_queue (
          id              BIGSERIAL PRIMARY KEY,
          queue           TEXT NOT NULL DEFAULT 'default',
          payload         JSONB NOT NULL,
          status          TEXT NOT NULL DEFAULT 'pending',
          run_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
          attempts        INT NOT NULL DEFAULT 0,
          max_attempts    INT NOT NULL DEFAULT 3,
          last_error      TEXT,
          created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
          updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """,
      )
      await conn.execute(
        """
        CREATE INDEX idx_job_queue_pending
        ON job_queue (status, run_at, id)
        WHERE status = 'pending';

        CREATE INDEX idx_job_queue_running_queue
        ON job_queue (queue)
        WHERE status = 'running';

        CREATE INDEX idx_job_queue_queue
        ON job_queue (queue);
        """,
      )
  except Exception as e:
    pass
  return pool

async def list(pool):
  async with pool.acquire() as conn:
    async for record in conn.cursor(
      """
      SELECT *
      FROM job_queue
      WHERE status != 'done';
      """,
    ):
      yield record

async def enqueue(pool, payload, queue="default", run_at=None):
  async with pool.acquire() as conn:
    row = await conn.fetchrow(
      """
      INSERT INTO job_queue (queue, payload, run_at)
      VALUES ($1, $2, COALESCE($3, now()))
      RETURNING
        id,
        queue,
        run_at,
        (
          SELECT count(*)
          FROM job_queue q
          WHERE
            q.queue = job_queue.queue
            AND q.status = 'pending'
            AND (
              q.run_at < job_queue.run_at
              OR (
                q.run_at = job_queue.run_at
                AND q.id < job_queue.id
              )
            )
        ) AS pending_ahead
      """,
      queue,
      payload,
      run_at,
    )
    return row["pending_ahead"]


async def dequeue(pool, max_per_image):
  async with pool.acquire() as conn:
    async with conn.transaction():
      row = await conn.fetchrow(
        """
        WITH candidate AS (
          SELECT jq.id, jq.queue
          FROM job_queue jq
          WHERE
            jq.status = 'pending'
            AND jq.run_at <= now()
            AND NOT EXISTS (
              SELECT 1
              FROM job_queue jq2
              WHERE
                jq2.queue = jq.queue
                AND jq2.status = 'running'
              GROUP BY jq2.queue
              HAVING count(*) >= $1
            )
          ORDER BY jq.id
          FOR UPDATE SKIP LOCKED
          LIMIT 1
        )
        UPDATE job_queue j
        SET
          status = 'running',
          attempts = attempts + 1,
          updated_at = now()
        FROM candidate c
        WHERE j.id = c.id
        RETURNING
          j.id,
          j.queue,
          j.payload
        """,
        max_per_image
      )
      return row

async def mark_done(pool, job_id):
  async with pool.acquire() as conn:
    await conn.execute(
      """
      UPDATE job_queue
      SET status = 'done',
        updated_at = now()
      WHERE id = $1
      """,
      job_id,
    )

async def mark_failed(pool, job_id, error):
  async with pool.acquire() as conn:
    await conn.execute(
      """
      UPDATE job_queue
      SET
        status = CASE
          WHEN attempts >= max_attempts THEN 'failed'
          ELSE 'pending'
        END,
        last_error = $1,
        updated_at = now(),
        run_at = now() + interval '30 seconds'
      WHERE id = $2
      """,
      error,
      job_id,
    )

async def worker(pool, handler, max_per_queue=1, poll_interval=1):
  while True:
    job = await dequeue(pool, max_per_queue)
    if job is None:
      await asyncio.sleep(poll_interval)
      continue
    try:
      await handler(job)
      await mark_done(pool, job['id'])
    except Exception as e:
      await mark_failed(pool, job['id'], str(e))

async def handle_job(job):
  from appyter.ext.emitter import url_to_emitter
  from appyter.execspec.core import url_to_executor
  payload = json.loads(job['payload'])
  async with url_to_executor(payload['executor']) as executor:
    async with url_to_emitter(payload['url']) as emitter:
      logger.info(f"Dispatching job {job['id']}")
      async for msg in executor._run(**payload):
        await emitter(msg)

core = web.Application()
routes = web.RouteTableDef()

@core.cleanup_ctx.append
async def _(app):
    app["db"] = await create_pool(app['config']['DATABASE_URL'])
    app["worker_tasks"] = [
       asyncio.create_task(worker(app["db"], handle_job, max_per_queue=int(app['config']['JOBS_PER_IMAGE'])))
       for _ in range(int(app['config']['JOBS']))
    ]
    try:
      yield
    finally:
      for task in app["worker_tasks"]:
        task.cancel()
      await app["db"].close()

@routes.get('/')
async def on_get(request):
  async with core['tasks'].lock:
    return web.json_response(dict(
      tasks=[record async for record in list(core['db'])],
      ts=datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc
      ).isoformat(),
    ))

@routes.post('/')
async def on_submit(request):
  job = await request.json()
  qsize = await enqueue(core['db'], job, job.get('executor'))
  return web.json_response(qsize)

core.add_routes(routes)
