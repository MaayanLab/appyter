import uuid
import logging
logger = logging.getLogger(__name__)

from appyter.ext.socketio import AsyncServer

socketio = AsyncServer(async_mode='aiohttp')

@socketio.on('connect')
async def _(sid, environ):
  request = environ['aiohttp.request']
  uid = request.headers.get('Authorization')
  if uid is None:
    uid = str(uuid.uuid4())
  logger.debug(f"connect: {uid} ({sid})")
  async with socketio.session(sid) as sess:
    sess['uid'] = uid
    sess['request_url'] = request_url = f"{request.scheme}://{request.host}{request.path}"
    if not request.app['config']['DEBUG']:
      public_url = request.app['config'].get('PUBLIC_URL')
      request_url = sess['request_url']
      if not public_url or not request_url.startswith(public_url):
        logger.warning(f"This could cause issues in production:\n{request_url=} {public_url=}")
    sess['config'] = request.app['config']
    sess['executor'] = request.app['executor']
  #
  from appyter.render.flask_app.room_manager import ensure_joined
  await ensure_joined(sid)
