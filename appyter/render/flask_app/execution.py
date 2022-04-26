import os
import asyncio
import traceback
import logging
logger = logging.getLogger(__name__)

from appyter.render.flask_app.prepare import _prepare_data, _prepare_request, _prepare_results, _prepare_storage, _prepare_executor
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
    instance_id = sanitize_sha1sum(data['_id'])
    assert instance_id is not None, 'Invalid session id'
    data.update(_config=config)
  else:
    data = dict(_config=config)
    data.update(await _prepare_data(data))
    data.update(await _prepare_request(data))
    instance_id = await _prepare_results(data)
  #
  if 'catalog-integration' in data['_config']['EXTRAS']:
    # if you execute the notebook, it should get registered
    #  we'll omit metadata which would already be captured
    #  when the instance was created
    try:
      from appyter.extras.catalog_integration.notebooks import InstanceInfo, add_instance
      await add_instance(
        InstanceInfo(instance=instance_id),
        auth=data.get('_auth'),
        config=data.get('_config'),
      )
    except:
      logger.warning(traceback.format_exc())
  #
  if await find_room(instance_id):
    await socketio.emit('status', 'Joining existing execution...', to=sid)
    await enter_room(sid, instance_id)
  else:
    try:
      storage = await _prepare_storage(data)
      async with _prepare_executor(data, executor) as executor:
        async with room_lock(instance_id):
          await enter_room(sid, instance_id)
          try:
            await socketio.emit('status', 'Submitting execution...', to=instance_id)
            job = dict(
              cwd=f"output/{instance_id}",
              ipynb=os.path.basename(config['IPYNB']),
              session=instance_id,
              id=generate_uuid(),
              url=join_url(request_url, instance_id),
              storage=storage,
              debug=config['DEBUG'],
            )
            async for msg in executor._run(**job):
              await socketio.forward(None, dict(event=msg['type'], data=msg['data'], to=instance_id))
          except asyncio.CancelledError:
            raise
          except Exception:
            logger.error(traceback.format_exc())
            await socketio.emit('error', 'An unhandled executor error occurred, please try again later.', to=sid)
    except asyncio.CancelledError:
      raise
    except:
      logger.error(traceback.format_exc())
      await socketio.emit('error', 'An unhandled initialization error occurred, please try again later.', to=sid)
      raise
