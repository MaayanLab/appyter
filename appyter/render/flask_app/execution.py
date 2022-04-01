import os
import asyncio
import traceback
import logging
logger = logging.getLogger(__name__)

from appyter.render.flask_app.prepare import _prepare_data, _prepare_results, _prepare_storage, _prepare_executor
from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.room_manager import enter_room, find_room, room_lock
from appyter.ext.uuid import sanitize_sha1sum, generate_uuid
from appyter.ext.urllib import join_url

# construct/join a notebook
@socketio.on('submit')
async def submit(sid, data):
  async with socketio.session(sid) as sess:
    config = sess['config']
    request_url = sess['request_url']
    executor = sess['executor']
  #
  if type(data) == str:
    data = dict(_id=data)
  elif type(data) != dict:
    raise Exception('Unrecognized data type')
  #
  if '_id' in data:
    result_hash = sanitize_sha1sum(data['_id'])
    assert result_hash is not None, 'Invalid session id'
    data.update(_config=config)
  else:
    data = dict(await _prepare_data(data), _config=config)
    result_hash = await _prepare_results(data)
  #
  if await find_room(result_hash):
    await socketio.emit('status', 'Joining existing execution...', to=sid)
    await enter_room(sid, result_hash)
  else:
    storage_uri = await _prepare_storage(data)
    async with _prepare_executor(data, executor) as executor:
      async with room_lock(result_hash):
        await enter_room(sid, result_hash)
        try:
          await socketio.emit('status', 'Submitting execution...', to=result_hash)
          job = dict(
            cwd=f"output/{result_hash}",
            ipynb=os.path.basename(config['IPYNB']),
            session=result_hash,
            id=generate_uuid(),
            url=join_url(request_url, result_hash),
            storage=storage_uri,
            debug=config['DEBUG'],
          )
          async for msg in executor._run(**job):
            await socketio.forward(None, dict(event=msg['type'], data=msg['data'], to=result_hash))
        except asyncio.CancelledError:
          raise
        except Exception:
          logger.error(traceback.format_exc())
          await socketio.emit('error', 'An unhandled executor error occurred, please try again later.', to=sid)
