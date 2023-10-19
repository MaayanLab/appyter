import logging
logger = logging.getLogger(__name__)

from appyter.ext.click import click_option_setenv
from appyter.orchestration.cli import orchestration
from appyter.orchestration.pg.schema import schema

@orchestration.command(help='Run the appyter pg woker')
@click_option_setenv('--database-url', envvar='APPYTER_DATABASE_URL', type=str, required=True, help='Postgres URI')
@click_option_setenv('--jobs', envvar='APPYTER_JOBS', type=int, default=2, help='Number of concurrent jobs to dispatch')
@click_option_setenv('--jobs-per-image', envvar='APPYTER_JOBS_PER_IMAGE', type=int, default=1, help='Number of concurrent jobs to dispatch for any individual appyter image')
@click_option_setenv('--debug', envvar='APPYTER_DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
async def worker(*args, **kwargs):
  import aiopg
  import asyncio
  from appyter.ext.emitter import url_to_emitter
  from appyter.execspec.core import url_to_executor
  async def pop(pool: aiopg.Pool):
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute('select pgp.pop();')
        async for id, job in cur:
          return id, job
  async def task_done(pool: aiopg.Pool, id):
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute('select pgp.task_done($1);', (id))
  async def requeue(pool: aiopg.Pool, id):
    async with pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute('select pgp.requeue($1);', (id))
  async def wait_for_work(pool: aiopg.Pool):
    async with pool.acquire() as conn:
      try:
        async with conn.cursor() as cur:
          await cur.execute(schema)
      except KeyboardInterrupt: raise
      except asyncio.CancelledError: raise
      except: pass # creating this schema/table will fail if it already exists
      #
      async with conn.cursor() as cur:
        await cur.execute('listen pgp')
        while True:
          msg = await conn.notifies.get()
          _channel, _msg_id, msg_kind = msg.payload.split(' ')
          if msg_kind == 'put':
            return
  async def work(id, job):
    async with url_to_executor(job['executor']) as executor:
      async with url_to_emitter(job['url']) as emitter:
        logger.info(f"Dispatching job {id}")
        async for msg in executor._run(**job):
          await emitter(msg)
  async def main():
    async with aiopg.create_pool(kwargs['database_url']) as pool:
      while True:
        id, job = await pop(pool)
        if id is None:
          try:
            await work(id, job)
          except:
            await requeue(pool, id)
            raise
          else:
            await task_done(pool, id)
        else:
          await wait_for_work(pool)
  asyncio.gather(*[
    main() for _ in range(kwargs['jobs'])
  ])
