import asyncio
import datetime
import functools
import importlib
from aiohttp import web
from collections import deque
from collections import OrderedDict, Counter
import logging
logger = logging.getLogger(__name__)

from appyter.orchestration.dispatcher.socketio import socketio

class LockedOrderedDict(OrderedDict):
  lock = asyncio.Lock()

# NOTE: This is questionable, this queue may run
#       on a different thread or process; in the case of a thread it's fine
#       because Queue is thread-safe, but not in the case of a process
#       we'd need a monkey-patched redis-Queue.
#

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
      debug=core['config']['DEBUG'],
      queued_ts=datetime.datetime.now().replace(
        tzinfo=datetime.timezone.utc
      ).isoformat(),
    )
  asyncio.create_task(core['dispatch_queue'].put(request_data['id']))
  return web.json_response(core['dispatch_queue'].qsize() + 1)

@core.on_startup.append
async def start_dispatchers(app):
  logger.info('Initializing dispatch...')
  #
  app['dispatch_queue'] = asyncio.Queue()
  app['tasks'] = LockedOrderedDict()
  #
  dispatch = functools.partial(
    importlib.import_module(
      '..dispatch.{}'.format(app['config']['DISPATCH']),
      __package__
    ).dispatch,
    debug=app['config']['DEBUG'],
    namespace=app['config']['KUBE_NAMESPACE'],
  )
  #
  logger.info('Starting background tasks...')
  for _ in range(app['config']['JOBS']):
    asyncio.create_task(
      dispatcher(
        queued=app['dispatch_queue'],
        tasks=app['tasks'],
        dispatch=dispatch,
        jobs_per_image=app['config']['JOBS_PER_IMAGE'],
      )
    )

core.add_routes(routes)

async def slow_put(queue, item):
  ''' Queue put debouncing
  '''
  await asyncio.sleep(1)
  await queue.put(item)

async def dispatcher(queued=None, tasks=None, dispatch=None, jobs_per_image=1):
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
      await dispatch(job=job)
    except:
      import traceback
      logger.error(f"dispatch error: {traceback.format_exc()}")
    #
    async with tasks.lock:
      del tasks[job_id]
  #
  job.task_done()
