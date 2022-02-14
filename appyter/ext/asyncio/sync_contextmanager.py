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

def sync_contextmanager_factory(async_contextmanager_factory):
  @contextlib.contextmanager
  def async_contextmanager_wrapper(*args, **kwargs):
    loop = asyncio.get_event_loop()
    async_contextmanager = async_contextmanager_factory(*args, **kwargs)
    ctx = loop.run_until_complete(async_contextmanager.__aenter__())
    try:
      yield ctx
    except:
      loop.run_until_complete(async_contextmanager.__aexit__(*sys.exc_info()))
    else:
      loop.run_until_complete(async_contextmanager.__aexit__(None, None, None))
  return async_contextmanager_wrapper
