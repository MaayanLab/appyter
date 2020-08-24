from socketio import AsyncServer

socketio = AsyncServer(async_mode='aiohttp')

@socketio.on('connect')
async def _(sid, environ):
  request = environ['aiohttp.request']
  print('connect', sid)
  async with socketio.session(sid) as sess:
    sess['request_url'] = str(request.url)
    sess['config'] = request.app['config']

@socketio.on('disconnect')
async def _(sid):
  print('disconnect', sid)
