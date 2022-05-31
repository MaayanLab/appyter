import socketio
import logging
logger = logging.getLogger(__name__)

from appyter.ext.socketio.priority_queued_emit import PriorityQueuedEmitMixin
from appyter.ext.socketio.chunked_emit import ChunkedEmitMixin

class AsyncServer(
  ChunkedEmitMixin,
  PriorityQueuedEmitMixin,
  socketio.AsyncServer,
):
  ''' Server with packet forwarding.
  `async with` is necessary for initialization
  '''
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self._listeners = { 'forward': [] }

  async def __aenter__(self):
    await super().__aenter__()
    super().on('forward')(self.forward)
    self._emit_enabled.set()
    return self
  
  async def __aexit__(self, *args):
    await super().__aexit__(*args)

  async def forward(self, sid, data):
    logger.debug(f"{sid} forward {data['event']} to {data['to']}")
    await super().emit(data['event'], data['data'], priority=max(0, data.get('priority', 0)) + 1, to=data['to'], skip_sid=sid)
    for listener in self._listeners['forward']:
      await listener(sid, data)

  def on(self, event):
    if event == 'forward':
      return self._listeners['forward'].append
    else:
      return super().on(event)
