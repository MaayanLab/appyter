from appyter.ext.socketio import AsyncServer

import logging
logger = logging.getLogger(__name__)

socketio = AsyncServer(async_mode='aiohttp')

@socketio.on('connect')
async def _(sid, environ):
  request = environ['aiohttp.request']
  logger.debug(f"connect: {sid}")
  async with socketio.session(sid) as sess:
    sess['request_url'] = f"{request.scheme}://{request.host}{request.path}"
    sess['config'] = request.app['config']

@socketio.on('disconnect')
async def _(sid):
  logger.debug(f"disconnect: {sid}")
