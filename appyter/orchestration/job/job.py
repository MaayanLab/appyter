import asyncio
import socketio
import urllib.parse
import logging
logger = logging.getLogger(__name__)

async def remote_message_producer(sio, msg_queue, job):
  @sio.event
  async def connect():
    await msg_queue.put(dict(type='connect', msg=''))
  @sio.event
  async def connect_error():
    await msg_queue.put(dict(type='connect_error', msg=''))
  @sio.event
  async def disconnect():
    await msg_queue.put(dict(type='disconnect', msg=''))
  @sio.event
  async def joined(data):
    await msg_queue.put(dict(type='joined', data=data))
  @sio.event
  async def left(data):
    await msg_queue.put(dict(type='left', data=data))
  #
  url = urllib.parse.urlparse(job['url'])
  await sio.connect(f"{url.scheme}://{url.netloc}", socketio_path=url.path)
  await sio.wait()

def emit_factory(msg_queue):
  async def emit(data):
    await msg_queue.put(dict(type='msg', data=data))
  return emit

def replay_nb_factory(msg_queue):
  ''' Setup a callback which will send the current notebook if someone joins the room
  '''
  async def replay_nb(get_nb):
    await msg_queue.put(dict(type='get_nb', data=get_nb))
  return replay_nb

async def evaluate_notebook(sio, msg_queue, job):
  from appyter.render.nbexecute import nbexecute_async
  await nbexecute_async(
    cwd=job['cwd'],
    emit=emit_factory(msg_queue),
    ipynb=job['ipynb'],
    subscribe_nb=replay_nb_factory(msg_queue),
  )
  await msg_queue.put(dict(type='stopped'))

async def evaluate_saga(sio, msg_queue, job):
  get_nb = None
  while msg := await msg_queue.get():
    logger.debug(msg)
    if msg['type'] == 'connect':
      await sio.emit('join', job['session'])
    elif msg['type'] == 'connect_error':
      raise Exception(str(msg))
    elif msg['type'] == 'joined' and msg['data']['session'] == job['session'] and msg['data']['id'] == sio.sid:
      sio.start_background_task(evaluate_notebook, sio, msg_queue, job)
    elif msg['type'] == 'get_nb':
      get_nb = msg['data']
    elif msg['type'] == 'joined' and callable(get_nb):
      await sio.emit('msg', dict(type='nb', data=get_nb(), to=msg['data']))
    elif msg['type'] == 'msg':
      await sio.emit('msg', dict(msg['data'], session=job['session']))
    elif msg['type'] == 'stopped':
      await sio.emit('leave', job['session'])
    elif msg['type'] == 'left' and msg['data']['session'] == job['session'] and msg['data']['id'] == sio.sid:
      await sio.disconnect()
    msg_queue.task_done()

async def execute_async(job):
  sio = socketio.AsyncClient(reconnection=False)
  msg_queue = asyncio.Queue()
  sio.start_background_task(remote_message_producer, sio, msg_queue, job)
  sio.start_background_task(evaluate_saga, sio, msg_queue, job)
  await sio.wait()

def execute(job):
  asyncio.run(execute_async(job), debug=job.get('DEBUG', False))
