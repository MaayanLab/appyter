import logging
from appyter.render.flask_app.socketio import socketio

logger = logging.getLogger(__name__)

@socketio.on('livereload')
async def _(sid, data):
  ''' Broadcast livereload packets in development
  '''
  async with socketio.session(sid) as sess:
    if not sess['config']['DEBUG']:
      return
  logger.info('Live reloading...')
  await socketio.emit('livereload', data)
