import json
import hashlib
import asyncio
import socketio
import logging
logger = logging.getLogger(__name__)

from appyter.ext.socketio.priority_queued_emit import PriorityQueuedEmitMixin

class AsyncClient(PriorityQueuedEmitMixin, socketio.AsyncClient):
  ''' Client with packet forwarding, emit buffering & chunking
  '''
  klass = socketio.AsyncClient
  CHUNK_SIZE = 1<<20 # 1 kb

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.connection_tracker()

  async def disconnect(self):
    logger.debug('Disconnecting...')
    if self._emit_enabled.is_set():
      logger.debug('Ensuring emit queue has been fully processed...')
      await self._emit_queue.join()
    logger.debug('Disconnect')
    await self.klass.disconnect(self)

  def connection_tracker(self):
    @self.event
    async def connect():
      self._emit_enabled.set()
    @self.event
    async def disconnect():
      self._emit_enabled.clear()

  async def _emit(self, evt, data, to=None, room=None, priority=0):
    if to is not None or room is not None:
      logger.debug('Client forwarding')
      await self._emit_queue.put((
        priority,
        next(self._emit_counter), 
        (
          'forward',
          dict(event=evt, data=data, to=to, room=room, priority=priority)
        ),
        dict()
      ))
    else:
      return await PriorityQueuedEmitMixin._emit(self, evt, data, to=to, room=room, priority=priority)

  async def emit(self, evt, data, priority=0, **kwargs):
    logger.debug('Client emit')
    serialized = json.dumps(data, sort_keys=True, separators=None, ensure_ascii=True)
    if len(serialized) > AsyncClient.CHUNK_SIZE:
      logger.debug(f"Large packet ({len(serialized)}), chunking...")
      sha1 = hashlib.sha1()
      sha1.update(serialized.encode())
      data_hash = sha1.hexdigest()
      n_chunks = len(serialized) // AsyncClient.CHUNK_SIZE + 1
      for n in range(0, n_chunks):
        await PriorityQueuedEmitMixin.emit(self,
          'chunked',
          dict(
            id=data_hash, event=evt, chunk=n, total=n_chunks,
            data=serialized[n*AsyncClient.CHUNK_SIZE:n*AsyncClient.CHUNK_SIZE+AsyncClient.CHUNK_SIZE]
          ),
          priority=priority+1,
          **kwargs,
        )
    else:
      await PriorityQueuedEmitMixin.emit(self, evt, data, priority=priority, **kwargs)
