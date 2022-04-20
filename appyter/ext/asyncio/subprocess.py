import asyncio
import logging
logger = logging.getLogger(__name__)

async def stream_readline_to_queue(stream, queue, chunk_size=65536):
  ''' Safely yield lines without running into buffer limit
  '''
  try:
    linebuf = b''
    while True:
      buf = await stream.read(chunk_size)
      if not buf: break
      linebuf += buf
      while True:
        msg, nl, rest = linebuf.partition(b'\n')
        if nl:
          await queue.put((msg + nl, False))
          linebuf = rest
        else:
          break
    if linebuf: await queue.put((linebuf, False))
  except Exception as e:
    await queue.put((e, True))
  else:
    await queue.put((None, True))

async def sh(*args, chunk_size=65536, **kwargs):
  ''' An opinionated asyncio shell that logs stderr & yields stdout, done
  Unlike standard create_subprocess_exec: LimitOverrunError should not be possible.
  '''
  stdout_queue = asyncio.Queue()
  logger.debug(' '.join(repr(arg) if ' ' in arg else arg for arg in args))
  proc = await asyncio.create_subprocess_exec(
    *args,
    stdout=asyncio.subprocess.PIPE,
    limit=chunk_size * 2,
    **kwargs,
  )
  reader = asyncio.create_task(stream_readline_to_queue(proc.stdout, stdout_queue, chunk_size=chunk_size))
  while True:
    msg, done = await stdout_queue.get()
    if isinstance(msg, bytes):
      yield msg, False
    elif isinstance(msg, Exception):
      raise msg
    stdout_queue.task_done()
    if done: break
  await reader
  yield await proc.wait(), True
