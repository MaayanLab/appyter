import random
import asyncio
import datetime
from aiohttp import web
from collections import OrderedDict, Counter
import logging
logger = logging.getLogger(__name__)

class LockedOrderedDict(OrderedDict):
  lock = asyncio.Lock()

core = web.Application()
routes = web.RouteTableDef()

@routes.get('/')
async def on_get(request):
  async with core['tasks'].lock:
    return web.json_response(dict(
      tasks=list(core['tasks'].values()),
      ts=datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc
      ).isoformat(),
    ))

@routes.post('/')
async def on_submit(request):
  request_data = await request.json()
  async with core['tasks'].lock:
    core['tasks'][request_data['id']] = dict(request_data,
      queued_ts=datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc
      ).isoformat(),
    )
  asyncio.create_task(core['dispatch_queue'].put(request_data['id']))
  return web.json_response(core['dispatch_queue'].qsize() + 1)

@core.cleanup_ctx.append
async def executor_ctx(app):
  logger.info('Initializing executor...')
  dispatch = app['config'].get('DISPATCH') or 'local'
  from appyter.execspec.core import url_to_executor
  async with url_to_executor(dispatch) as executor:
    app['executor'] = executor
    yield

@core.cleanup_ctx.append
async def dispatcher_ctx(app):
  logger.info('Initializing dispatcher...')
  #
  app['dispatch_queue'] = asyncio.Queue()
  app['tasks'] = LockedOrderedDict()
  #
  logger.info('Starting background tasks...')
  tasks = [
    asyncio.create_task(
      dispatcher(
        queued=app['dispatch_queue'],
        tasks=app['tasks'],
        executor=app['executor'],
        jobs_per_image=app['config']['JOBS_PER_IMAGE'],
      )
    )
    for _ in range(app['config']['JOBS'])
  ]
  yield
  await app['dispatch_queue'].join()
  for task in tasks:
    try:
      task.cancel()
      await task
    except asyncio.CancelledError:
      pass

core.add_routes(routes)

async def slow_put(queue, item):
  ''' Queue put debouncing
  '''
  await asyncio.sleep(0.5 + random.random())
  await queue.put(item)

async def dispatcher(queued=None, tasks=None, executor=None, jobs_per_image=1):
  while True:
    job_id = await queued.get()
    async with tasks.lock:
      job = tasks[job_id]
      image_jobs = Counter(t.get('image') for t in tasks.values() if 'started_ts' in t).get(job.get('image'), 0)
      if image_jobs >= jobs_per_image:
        # TODO: push back onto a priority queue such that the next slot that opens uses this one
        #       currently, this appyter execution would end up on the back of the queue
        queued.task_done()
        asyncio.create_task(slow_put(queued, job_id))
        continue
      else:
        tasks[job['id']]['started_ts'] = datetime.datetime.now().replace(
          tzinfo=datetime.timezone.utc
        ).isoformat()
    #
    try:
      logger.info(f"Dispatching job {job_id}")
      async for status in executor.run(job):
        # TODO: phone-home with status?
        pass
    except asyncio.CancelledError:
      raise
    except:
      import traceback
      logger.error(f"dispatch error: {traceback.format_exc()}")
    #
    async with tasks.lock:
      del tasks[job_id]
