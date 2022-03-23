import asyncio
import urllib.parse
import logging
logger = logging.getLogger(__name__)

async def setup_evaluate_notebook(emitter, job):
  from appyter.render.nbexecute import nbexecute_async
  state = dict(get_state=None)
  # state is ready -- get a reference to it
  @emitter.on('get_state')
  async def on_get_state(get_state=None, **kwargs):
    state['get_state'] = get_state
  # someone joins, send them the notebook, state
  @emitter.on('joined')
  async def on_joined(id=None, **kwargs):
    if state.get('get_state'):
      nb_state = state['get_state']()
      await emitter.emit('msg', type='nb', data=nb_state['nb'], to=id)
      await emitter.emit('msg', type='status', data=nb_state['status'], to=id)
      await emitter.emit('msg', type='progress', data=nb_state['progress'], to=id)
  #
  async def emit(data):
    await emitter.emit('msg', **data)
  #
  async def subscribe(get_state):
    await emitter.emit('get_state', get_state=get_state)
  #
  await nbexecute_async(
    cwd=job['cwd'],
    ipynb=job['ipynb'],
    emit=emit,
    subscribe=subscribe,
    fuse=not job.get('debug', False),
  )
  await emitter.emit('stopped')

async def setup_socketio(emitter, job):
  from appyter.ext.socketio import AsyncClient
  async with AsyncClient() as sio:
    #
    @sio.event
    async def joined(data):
      if data['id'] != sio.sid:
        await emitter.emit('joined', id=data['id'])
    #
    @emitter.on('msg')
    async def on_msg(type=None, data=None, to=None, **kwargs):
      await sio.emit(type, data, priority=1, to=to if to is not None else job['session'], **kwargs)
    #
    url = urllib.parse.urlparse(job['url'])
    await sio.connect(f"{url.scheme}://{url.netloc}", socketio_path=url.path)
    await sio.emit('join', job['session'])
    await emitter.wait('stopped')
    await emitter.flush()
    await emitter.clear()
    await sio.disconnect()

async def execute_async(job, debug=False):
  from appyter.ext.asyncio.event_emitter import EventEmitter
  from appyter.ext.fsspec.storage import ensure_storage
  emitter = EventEmitter()
  logger.debug(job)
  async with ensure_storage(job['storage']):
    await asyncio.gather(
      setup_evaluate_notebook(emitter, job),
      setup_socketio(emitter, job),
    )
    logger.debug('EXITING')

def execute(job):
  from appyter.ext.asyncio.helpers import ensure_sync
  from appyter.ext.asyncio.event_loop import with_event_loop
  debug = job.get('debug', False)
  with with_event_loop():
    ensure_sync(execute_async(job, debug=debug))
