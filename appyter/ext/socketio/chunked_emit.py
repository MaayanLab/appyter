import json
import logging

from appyter.ext.asyncio.helpers import ensure_async
from appyter.ext.hashlib import sha1sum_str
logger = logging.getLogger(__name__)

class ChunkedEmitMixin:
  ''' A mixin for splitting up large `emit` calls into `chunked` calls of lower priority
  '''
  CHUNK_SIZE = 1<<20 # 1kb
  CHUNK_OVERHEAD = 1<<8 # not worth it if it doesn't exceed overhead

  async def emit(self, evt, data, priority=0, **kwargs):
    chunkable = evt not in {'chunked', 'forward'}
    if chunkable:
      serialized = await ensure_async(json.dumps)(data, sort_keys=True, separators=None, ensure_ascii=True)
      chunkable = len(serialized) > (self.CHUNK_SIZE + self.CHUNK_OVERHEAD)
    #
    if chunkable:
      logger.debug(f"Large packet ({len(serialized)}), chunking...")
      data_hash = await ensure_async(sha1sum_str)(serialized)
      n_chunks = (len(serialized) // ChunkedEmitMixin.CHUNK_SIZE) + int(len(serialized) % ChunkedEmitMixin.CHUNK_SIZE != 0)
      for n in range(0, n_chunks):
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
