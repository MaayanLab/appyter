import uuid
import traceback
import socketio
import logging
logger = logging.getLogger(__name__)

from appyter.ext.socketio.forwarding import ForwardingMixin
from appyter.ext.socketio.priority_queued_emit import PriorityQueuedEmitMixin
from appyter.ext.socketio.chunked_emit import ChunkedEmitMixin

class AsyncClient(
  ChunkedEmitMixin,
  ForwardingMixin,
  PriorityQueuedEmitMixin,
  socketio.AsyncClient,
):
  ''' Client with packet forwarding, emit buffering & chunking
   `async with` is necessary for initialization
  '''
  async def __aenter__(self):
    await super().__aenter__()
    #
    @self.event
    async def connect():
      self._emit_enabled.set()
    @self.event
    async def disconnect():
      self._emit_enabled.clear()
    #
    return self

  async def __aexit__(self, *args):
    await super().__aexit__(*args)
    try: await self.eio.http.close()
    except: logger.warn(traceback.format_exc())

  async def connect(self, *args, headers={}, **kwargs):
    return await super().connect(
      *args,
      headers=dict({ 'Authorization': str(uuid.uuid4()) }, **headers),
      **kwargs,
    )
