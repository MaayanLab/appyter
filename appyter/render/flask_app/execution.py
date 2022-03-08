import os
import asyncio
import traceback
import logging
logger = logging.getLogger(__name__)

from appyter.render.flask_app.core import prepare_data, prepare_results
from appyter.render.flask_app.socketio import socketio
from appyter.ext.uuid import sanitize_sha1sum, generate_uuid
from appyter.ext.urllib import join_slash, join_url

# construct/join a notebook
@socketio.on('submit')
async def submit(sid, data):
  async with socketio.session(sid) as sess:
    config = sess['config']
    request_url = sess['request_url']
    executor = sess['executor']
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
  await socketio.emit('status', 'Queuing execution', to=sid)
  job = dict(
    cwd=join_url('storage://output/', result_hash),
    ipynb=os.path.basename(config['IPYNB']),
    session=result_hash,
    id=generate_uuid(),
    url=request_url,
    image=config.get('DISPATCHER_IMAGE'),
    storage=config['DATA_DIR'],
    debug=config['DEBUG'],
  )
  try:
    await executor.submit(job)
    await socketio.emit('status', f"Queued successfully, your execution will begin when resources are available.", to=sid)
  except asyncio.CancelledError:
    raise
  except Exception:
    logger.error(traceback.format_exc())
    await socketio.emit('error', 'Failed to submit job, please try again later.', to=sid)

@socketio.on('join')
async def _(sid, data):
  socketio.enter_room(sid, data)
  await socketio.emit('joined', dict(id=sid, session=data), to=data)
