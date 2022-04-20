import os
import asyncio

COPY_BUFSIZE = 1024 * 1024 if os.name == 'posix' else 64 * 1024

async def async_copyfileobj(fsrc, fdst, length=0):
  ''' Async version of shutil.copyfileobj
  '''
  if not length:
    length = COPY_BUFSIZE
  fsrc_read = fsrc.read
  fdst_write = fdst.write
  while True:
    buf = fsrc_read(length)
    if not buf:
      break
    await asyncio.sleep(0)
    fdst_write(buf)
    await asyncio.sleep(0)
