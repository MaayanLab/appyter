import os
import aiohttp
from subprocess import PIPE

from appyter.render.flask_app.core import prepare_data, prepare_results
from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.util import sanitize_sha1sum, generate_uuid, join_routes
from appyter.ext.fs import Filesystem

# construct/join a notebook
@socketio.on('submit')
async def submit(sid, data):
  async with socketio.session(sid) as sess:
    config = sess['config']
  #
  if type(data) == dict:
    data = prepare_data(data)
    result_hash = prepare_results(data)
  elif type(data) == str:
    result_hash = sanitize_sha1sum(data)
    assert result_hash is not None
  else:
    raise Exception('Unrecognized data type')
  #
  # TODO: submit job iff it hasn't already been executed
  socketio.enter_room(sid, result_hash)
  await socketio.emit('status', 'Queuing execution', room=result_hash)
  job = dict(
    cwd=Filesystem.join(config['DATA_DIR'], 'output', result_hash),
    ipynb=os.path.basename(config['IPYNB']),
    session=result_hash,
    job=generate_uuid(),
  )
  if config['DISPATCHER_URL']:
    job['url'] = join_routes(config['DISPATCHER_URL'], 'socket.io') + '/'
  if config['DISPATCHER_IMAGE']:
    job['image'] = config['DISPATCHER_IMAGE']
  #
  # TODO: worry about inaccessible dispatcher
  if config['DISPATCHER']:
    async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as client:
      async with client.post(config['DISPATCHER'], json=job) as resp:
        queue_size = await resp.json()
        # TODO: keep track of queue position?
        await socketio.emit('status', f"Queued successfully, you are at position {queue_size} in the queue", room=result_hash)
  else:
    from appyter.orchestration.job.job import execute_async
    await execute_async(job)

@socketio.on('join')
async def _(sid, data):
  session = data['session']
  job = data['job']
  socketio.enter_room(sid, session)
  await socketio.emit('joined', job, room=session)

@socketio.on('message')
async def _(sid, data):
  await socketio.emit(data['type'], data['data'], room=data['session'])
