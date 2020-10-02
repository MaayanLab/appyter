import asyncio
import socketio
import urllib.parse
import itertools as it
import logging
logger = logging.getLogger(__name__)

async def remote_message_producer(sio, msg_queue, msg_counter, job):
  @sio.event
  async def connect():
    await msg_queue.put((1, next(msg_counter), dict(type='connect', msg='')))
  @sio.event
  async def connect_error():
    await msg_queue.put((0, next(msg_counter), dict(type='connect_error', msg='')))
  @sio.event
  async def disconnect():
    await msg_queue.put((0, next(msg_counter), dict(type='disconnect', msg='')))
  @sio.event
  async def joined(data):
    await msg_queue.put((1, next(msg_counter), dict(type='joined', data=data)))
  @sio.event
  async def left(data):
    await msg_queue.put((8, next(msg_counter), dict(type='left', data=data)))
  #
  url = urllib.parse.urlparse(job['url'])
  await sio.connect(f"{url.scheme}://{url.netloc}", socketio_path=url.path)
  await sio.wait()

def emit_factory(msg_queue, msg_counter):
  async def emit(data):
    await msg_queue.put((5, next(msg_counter), dict(type='msg', data=data)))
  return emit

def replay_nb_factory(msg_queue, msg_counter):
  ''' Setup a callback which will send the current notebook if someone joins the room
  '''
  async def replay_nb(get_nb):
    await msg_queue.put((2, next(msg_counter), dict(type='get_nb', data=get_nb)))
  return replay_nb

async def evaluate_notebook(sio, msg_queue, msg_counter, job):
  from appyter.render.nbexecute import nbexecute_async
  await nbexecute_async(
    cwd=job['cwd'],
    emit=emit_factory(msg_queue, msg_counter),
    ipynb=job['ipynb'],
    subscribe_nb=replay_nb_factory(msg_queue, msg_counter),
  )
  await msg_queue.put((10, next(msg_counter), dict(type='stopped')))

async def evaluate_saga(sio, msg_queue, msg_counter, job):
  get_nb = None
  while priority_msg := await msg_queue.get():
    _, _, msg = priority_msg
    if msg['type'] == 'connect':
      await sio.emit('join', job['session'])
    elif msg['type'] == 'connect_error':
      raise Exception(str(msg))
    elif msg['type'] == 'joined' and msg['data']['session'] == job['session'] and msg['data']['id'] == sio.sid:
      sio.start_background_task(evaluate_notebook, sio, msg_queue, msg_counter, job)
    elif msg['type'] == 'get_nb':
      get_nb = msg['data']
    elif msg['type'] == 'joined' and msg['data']['session'] == job['session'] and callable(get_nb):
      await sio.emit('msg', dict(type='nb', data=get_nb(), to=msg['data']['id']))
    elif msg['type'] == 'msg':
      await sio.emit('msg', dict(msg['data'], session=job['session']))
    elif msg['type'] == 'stopped':
      await sio.emit('leave', job['session'])
    elif msg['type'] == 'left' and msg['data']['session'] == job['session'] and msg['data']['id'] == sio.sid:
      await sio.disconnect()
    elif msg['type'] == 'disconnect':
      msg_queue.task_done()
      return
    msg_queue.task_done()

async def execute_async(job):
  sio = socketio.AsyncClient(reconnection=False)
  msg_queue = asyncio.PriorityQueue()
  msg_counter = it.count()
  sio.start_background_task(remote_message_producer, sio, msg_queue, msg_counter, job)
  try:
    await evaluate_saga(sio, msg_queue, msg_counter, job)
    await sio.wait()
  except asyncio.CancelledError:
    raise

def execute(job):
  asyncio.run(execute_async(job), debug=job.get('DEBUG', False))
