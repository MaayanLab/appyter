import sys
import asyncio
import contextlib

@contextlib.contextmanager
def sync_contextmanager(async_contextmanager):
  loop = asyncio.get_event_loop()
  ctx = loop.run_until_complete(async_contextmanager.__aenter__())
  try:
    yield ctx
  except:
    loop.run_until_complete(async_contextmanager.__aexit__(*sys.exc_info()))
  else:
    loop.run_until_complete(async_contextmanager.__aexit__(None, None, None))
