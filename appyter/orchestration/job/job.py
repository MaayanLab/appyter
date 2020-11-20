import asyncio
import socketio
import urllib.parse
import itertools as it
import logging
logger = logging.getLogger(__name__)

from appyter.ext.asyncio.event_emitter import EventEmitter


def setup_socketio_events(sio, emitter):
  @sio.event
  async def connect():
    await emitter.emit('connect')
  @sio.event
  async def connect_error(error):
    await emitter.emit('connect_error', error=error)
  @sio.event
  async def disconnect():
    await emitter.emit('disconnect')
  @sio.event
  async def joined(data):
    await emitter.emit('joined', data=data)
  @sio.event
  async def left(data):
    await emitter.emit('left', data=data)


def emit_factory(emitter):
  async def emit(data):
    await emitter.emit('msg', data=data)
  return emit

def get_state_factory(emitter):
  ''' Setup a callback which will send the current notebook if someone joins the room
  '''
  async def subscribe(get_state):
    await emitter.emit('get_state', data=get_state)
  return subscribe

async def evaluate_notebook(sio, emitter, job):
  from appyter.render.nbexecute import nbexecute_async
  await nbexecute_async(
    cwd=job['cwd'],
    emit=emit_factory(emitter),
    ipynb=job['ipynb'],
    subscribe=get_state_factory(emitter),
  )
  await emitter.emit('stopped')

def setup_execute_async(sio, emitter, job):
  client_lock = asyncio.Lock()
  state_lock = asyncio.Lock()
  state = dict(executed=False, get_state=None)
  connected = asyncio.Event()
  joined = asyncio.Event()
  #
  @emitter.on('connect')
  async def on_connect(**kwargs):
    connected.set()
    async with client_lock:
      await sio.emit('join', job['session'])
  @emitter.on('connect_error')
  async def on_connect_error(error, **kwargs):
    connected.clear()
    logger.error(error)
  @emitter.on('disconnect')
  async def on_disconnect(**kwargs):
    joined.clear()
    connected.clear()
  @emitter.on('joined')
  async def on_joined(data={}, **kwargs):
    if data['session'] == job['session'] and data['id'] == sio.sid:
      joined.set()
      async with state_lock:
        if not state['executed']:
          state['executed'] = True
          asyncio.create_task(evaluate_notebook(sio, emitter, job))
    elif callable(state['get_state'], **kwargs):
      async with state_lock:
        nb_state = state['get_state']()
        await connected.wait()
        async with client_lock:
          await sio.emit('msg', dict(type='nb', data=nb_state['nb'], to=data['id']))
        await connected.wait()
        async with client_lock:
          await sio.emit('msg', dict(type='status', data=nb_state['status'], to=data['id']))
        await connected.wait()
        async with client_lock:
          await sio.emit('msg', dict(type='progress', data=nb_state['progress'], to=data['id']))
  @emitter.on('get_state')
  async def on_get_state(data=None, **kwargs):
    async with state_lock:
      state['get_state'] = data
  @emitter.on('msg')
  async def on_msg(data={}, **kwargs):
    await connected.wait()
    await joined.wait()
    async with client_lock:
      await sio.emit('msg', dict(data, session=job['session']))
  @emitter.on('joined')
  async def on_joined(data=None, **kwargs):
    state['joined'] = data
  @emitter.on('stopped')
  async def on_stopped(**kwargs):
    await connected.wait()
    await joined.wait()
    async with client_lock:
      await sio.emit('leave', job['session'])
  @emitter.on('left')
  async def on_left(data={}, **kwargs):
    if data['session'] == job['session'] and data['id'] == sio.sid:
      async with client_lock:
        await sio.disconnect()

async def execute_async(job, debug=False):
  sio = socketio.AsyncClient()
  emitter = EventEmitter()
  #
  try:
    setup_socketio_events(sio, emitter)
    setup_execute_async(sio, emitter, job)
    url = urllib.parse.urlparse(job['url'])
    await sio.connect(f"{url.scheme}://{url.netloc}", socketio_path=url.path)
    await sio.wait()
    await emitter.clear()
  except asyncio.CancelledError:
    raise

def execute(job):
  debug = job.get('debug', False)
  logging.basicConfig(level=logging.DEBUG if debug else logging.WARNING)
  logger.info(job)
  asyncio.run(execute_async(job, debug=debug))
