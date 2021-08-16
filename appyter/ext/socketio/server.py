import socketio
import logging
logger = logging.getLogger(__name__)

from appyter.ext.socketio.priority_queued_emit import PriorityQueuedEmitMixin

class AsyncServer(PriorityQueuedEmitMixin, socketio.AsyncServer):
  ''' Server with packet forwarding
  '''
  klass = socketio.AsyncServer

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._emit_enabled.set()
    #
    this = self
    @self.on('forward')
    async def forward(sid, data):
      logger.debug('Server forward')
      if data.get('to'):
        await this.emit(data['event'], data['data'], priority=max(0, data.get('priority', 0)) + 1, to=data['to'])
      elif data.get('room'):
        await this.emit(data['event'], data['data'], priority=max(0, data.get('priority', 0)) + 1, room=data['room'])
