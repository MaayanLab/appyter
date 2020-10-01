import os
import aiohttp
import asyncio
import traceback
from subprocess import PIPE
import logging
logger = logging.getLogger(__name__)

from appyter.render.flask_app.core import prepare_data, prepare_results
from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.util import sanitize_sha1sum, generate_uuid, join_routes
from appyter.ext.fs import Filesystem

# construct/join a notebook
@socketio.on('submit')
async def submit(sid, data):
  async with socketio.session(sid) as sess:
    config = sess['config']
    request_url = sess['request_url']
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
  socketio.enter_room(sid, result_hash)
  await socketio.emit('status', 'Queuing execution', sid)
  job = dict(
    cwd=Filesystem.join(config['DATA_DIR'], 'output', result_hash),
    ipynb=os.path.basename(config['IPYNB']),
    session=result_hash,
    id=generate_uuid(),
  )
  #
  if config['DISPATCHER_URL']:
    job['url'] = join_routes(config['DISPATCHER_URL'], 'socket.io').lstrip('/') + '/'
  else:
    job['url'] = request_url
  #
  if config['DISPATCHER_IMAGE']:
    job['image'] = config['DISPATCHER_IMAGE']
  #
  if config['DISPATCHER']:
    queued = False
    backoff = 1
    while not queued:
      try:
        async with aiohttp.ClientSession(headers={'Content-Type': 'application/json'}) as client:
          async with client.post(config['DISPATCHER'], json=job) as resp:
            queue_size = await resp.json()
            await socketio.emit('status', f"Queued successfully, you are at position {queue_size} in the queue", sid)
            queued = True
      except Exception:
        logger.error(traceback.format_exc())
        if backoff < 60:
          await socketio.emit('status', f"Failed to contact orchestrator, trying again in {backoff}s...", sid)
          asyncio.sleep(backoff)
          backoff *= 2
        else:
          await socketio.emit('error', 'Failed to contact orchestrator, please try again later.', sid)
          break
  else:
    from appyter.orchestration.job.job import execute_async
    await execute_async(job)

@socketio.on('join')
async def _(sid, data):
  id = data.get('id', sid)
  session = data['session']
  socketio.enter_room(sid, session)
  await socketio.emit('joined', id, room=session)

@socketio.on('leave')
async def _(sid, data):
  id = data.get('id', sid)
  session = data['session']
  await socketio.emit('left', id, room=session)
  socketio.leave_room(sid, session)

@socketio.on('msg')
async def _(sid, data):
  await socketio.emit(data['type'], data['data'], room=data['session'])
