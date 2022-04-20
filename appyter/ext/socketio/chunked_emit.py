import json
import uuid
import logging
import asyncio

logger = logging.getLogger(__name__)

class ChunkedEmitMixin:
  ''' A mixin for splitting up large `emit` calls into `chunked` calls of lower priority
  '''
  CHUNK_SIZE = 1<<20 # 1kb

  async def emit(self, evt, data, priority=0, **kwargs):
    chunkable = evt not in {'chunked', 'forward'}
    if chunkable:
      serialized = json.dumps(data, sort_keys=True, separators=None, ensure_ascii=True)
      chunkable = len(serialized) > self.CHUNK_SIZE
      await asyncio.sleep()
    #
    if chunkable:
      logger.debug(f"Large packet ({len(serialized)}), chunking...")
      data_hash = str(uuid.uuid4())
      n_chunks = (len(serialized) // ChunkedEmitMixin.CHUNK_SIZE) + int(len(serialized) % ChunkedEmitMixin.CHUNK_SIZE != 0)
      for n in range(0, n_chunks):
        await asyncio.sleep()
        await super().emit(
          'chunked',
          dict(
            id=data_hash, event=evt, chunk=n, total=n_chunks,
            data=serialized[n*self.CHUNK_SIZE:(n+1)*self.CHUNK_SIZE]
          ),
          priority=priority+1,
          **kwargs,
        )
    else:
      await super().emit(evt, data, priority=priority, **kwargs)
