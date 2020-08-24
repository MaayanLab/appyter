import asyncio
import socketio

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
  #
  await sio.connect(job['url'])
  await sio.wait()

def emit_factory(sio, session):
  async def emit(data):
    await sio.emit('message', dict(data, session=session))
  return emit

async def evaluate_saga(sio, msg_queue, job):
  from appyter.render.nbexecute import nbexecute_async
  #
  while msg := await msg_queue.get():
    if msg['type'] == 'connect':
      await sio.emit('join', dict(session=job['session'], job=job['job']))
    elif msg['type'] == 'connect_error':
      raise Exception(str(msg))
    elif msg['type'] == 'joined' and msg['data'] == job['job']:
      await nbexecute_async(
        ipynb=job['ipynb'],
        emit=emit_factory(sio, job['session']),
        cwd=job['cwd'],
      )
      await sio.disconnect()
    msg_queue.task_done()

async def execute_async(job):
  sio = socketio.AsyncClient(reconnection=False)
  msg_queue = asyncio.Queue()
  producers = [
    asyncio.create_task(remote_message_producer(sio, msg_queue, job))
  ]
  consumers = [
    asyncio.create_task(evaluate_saga(sio, msg_queue, job)),
  ]
  await asyncio.gather(*producers)
  await msg_queue.join()
  for c in consumers:
    c.cancel()

def execute(job):
  asyncio.run(execute_async(job), debug=job.get('DEBUG', False))
