import json
import hashlib
import logging
logger = logging.getLogger(__name__)

class ChunkedEmitMixin:
  ''' A mixin for splitting up large `emit` calls into `chunked` calls of lower priority
  '''
  CHUNK_SIZE = 1<<20 # 1 kb
  CHUNK_PADDING = 1<<8 # don't re-chunk forwarded chunks, size of padding around the chunk

  async def emit(self, evt, data, priority=0, **kwargs):
    serialized = json.dumps(data, sort_keys=True, separators=None, ensure_ascii=True)
    if len(serialized) > self.CHUNK_SIZE + self.CHUNK_PADDING:
      logger.debug(f"Large packet ({len(serialized)}), chunking...")
      sha1 = hashlib.sha1()
      sha1.update(serialized.encode())
      data_hash = sha1.hexdigest()
      n_chunks = len(serialized) // ChunkedEmitMixin.CHUNK_SIZE + 1
      for n in range(0, n_chunks):
        await super().emit(
          'chunked',
          dict(
            id=data_hash, event=evt, chunk=n, total=n_chunks,
            data=serialized[n*self.CHUNK_SIZE:n*self.CHUNK_SIZE+self.CHUNK_SIZE]
          ),
          priority=priority+1,
          **kwargs,
        )
    else:
      await super().emit(evt, data, priority=priority, **kwargs)
