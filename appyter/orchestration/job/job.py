import asyncio
import socketio
import urllib.parse
import itertools as it
import logging
logger = logging.getLogger(__name__)

class OrderedPriorityQueue(asyncio.PriorityQueue):
  def __init__(self):
    super().__init__()
    self._msg_counter = it.count()
  #
  async def put(self, msg, priority=0, count=None):
    if count is None:
      count = next(self._msg_counter)
    return await super().put((priority, count, msg))
  #
  async def get(self):
    return await super().get()

async def remote_message_producer(sio, msg_queue, job):
  @sio.event
  async def connect():
    await msg_queue.put(dict(type='connect', msg=''), priority=1)
  @sio.event
  async def connect_error():
    await msg_queue.put(dict(type='connect_error', msg=''), priority=0)
  @sio.event
  async def disconnect():
    await msg_queue.put(dict(type='disconnect', msg=''), priority=0)
  @sio.event
  async def joined(data):
    await msg_queue.put(dict(type='joined', data=data), priority=1)
  @sio.event
  async def left(data):
    await msg_queue.put(dict(type='left', data=data), priority=8)
  #
  url = urllib.parse.urlparse(job['url'])
  await sio.connect(f"{url.scheme}://{url.netloc}", socketio_path=url.path)
  await sio.wait()

def emit_factory(msg_queue):
  async def emit(data):
    await msg_queue.put(dict(type='msg', data=data), priority=5)
  return emit

def get_state_factory(msg_queue):
  ''' Setup a callback which will send the current notebook if someone joins the room
  '''
  async def subscribe(get_state):
    await msg_queue.put(dict(type='get_state', data=get_state), priority=2)
  return subscribe

async def evaluate_notebook(sio, msg_queue, job):
  from appyter.render.nbexecute import nbexecute_async
  await nbexecute_async(
    cwd=job['cwd'],
    emit=emit_factory(msg_queue),
    ipynb=job['ipynb'],
    subscribe=get_state_factory(msg_queue),
  )
  await msg_queue.put(dict(type='stopped'), priority=10)

async def evaluate_saga(sio, msg_queue, job):
  connected = False
  joined = False
  executed = False
  get_state = None
  while prioritized_msg := await msg_queue.get():
    priority, count, msg = prioritized_msg
    logger.debug(msg)
    if msg['type'] == 'connect':
      connected = True
      await sio.emit('join', job['session'])
    elif msg['type'] == 'connect_error':
      raise Exception(str(msg))
    elif msg['type'] == 'disconnect':
      connected = False
      joined = False
      await asyncio.sleep(0.1)
    elif not connected:
      await msg_queue.put(msg, priority=priority, count=count)
      await asyncio.sleep(0.1)
    elif msg['type'] == 'joined' and msg['data']['session'] == job['session'] and msg['data']['id'] == sio.sid:
      joined = True
      if not executed:
        sio.start_background_task(evaluate_notebook, sio, msg_queue, job)
        executed = True
    elif not joined:
      await msg_queue.put(msg, priority=priority, count=count)
      await asyncio.sleep(0.1)
    elif msg['type'] == 'get_state':
      get_state = msg['data']
    elif msg['type'] == 'joined' and msg['data']['session'] == job['session'] and callable(get_state):
      state = get_state()
      await sio.emit('msg', dict(type='nb', data=state['nb'], to=msg['data']['id']))
      await sio.emit('msg', dict(type='status', data=state['status'], to=msg['data']['id']))
      await sio.emit('msg', dict(type='progress', data=state['progress'], to=msg['data']['id']))
    elif msg['type'] == 'msg':
      await sio.emit('msg', dict(msg['data'], session=job['session']))
    elif msg['type'] == 'stopped':
      await sio.emit('leave', job['session'])
    elif msg['type'] == 'left' and msg['data']['session'] == job['session'] and msg['data']['id'] == sio.sid:
      await sio.disconnect()
      msg_queue.task_done()
      return
    msg_queue.task_done()

async def execute_async(job):
  sio = socketio.AsyncClient()
  msg_queue = OrderedPriorityQueue()
  sio.start_background_task(remote_message_producer, sio, msg_queue, job)
  try:
    await evaluate_saga(sio, msg_queue, job)
    await sio.wait()
  except asyncio.CancelledError:
    raise

def execute(job):
  asyncio.run(execute_async(job), debug=job.get('DEBUG', False))
