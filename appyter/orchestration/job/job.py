import asyncio
import urllib.parse
import itertools as it
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
    if 'get_state' in state:
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
  )
  await emitter.emit('stopped')

async def setup_socketio(emitter, job):
  from appyter.ext.socketio import AsyncClient
  sio = AsyncClient()
  #
  @sio.event
  async def joined(data):
    if data['id'] != sio.sid:
      await emitter.emit('joined', id=data['id'])
  #
  @emitter.on('msg')
  async def on_msg(type=None, data=None, to=None, room=None, **kwargs):
    if to is not None:
      await sio.emit(type, data, priority=1, to=to, **kwargs)
    else:
      await sio.emit(type, data, priority=1, room=job['session'], **kwargs)
  #
  url = urllib.parse.urlparse(job['url'])
  await sio.connect(f"{url.scheme}://{url.netloc}", socketio_path=url.path)
  await sio.emit('join', job['session'])
  await emitter.wait('stopped')
  await emitter.flush()
  await sio.disconnect()

async def execute_async(job, debug=False):
  from appyter.ext.asyncio.event_emitter import EventEmitter
  emitter = EventEmitter()
  await asyncio.gather(
    setup_evaluate_notebook(emitter, job),
    setup_socketio(emitter, job),
  )
  logger.debug('EXITING')

def execute(job):
  debug = job.get('debug', False)
  logging.basicConfig(
    level=logging.DEBUG if debug else logging.WARNING,
    format='%(name)s %(message).80s',
  )
  logger.info(job)
  loop = asyncio.get_event_loop()
  loop.run_until_complete(execute_async(job, debug=debug))
