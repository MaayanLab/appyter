import logging
logger = logging.getLogger(__name__)

def try_n_times(n, func, *args, **kwargs):
  import time
  backoff = 1
  while n > 0:
    try:
      return func(*args, **kwargs)
    except KeyboardInterrupt:
      raise
    except Exception as err:
      n -= 1
      if n == 0:
        raise err
      logger.warning(f"{func} failed, trying again in {backoff}s...")
      time.sleep(backoff)
      backoff *= 2

async def async_try_n_times(n, coro, *args, **kwargs):
  import asyncio
  backoff = 1
  while n > 0:
    try:
      return await coro(*args, **kwargs)
    except asyncio.CancelledError:
      raise
    except Exception as err:
      n -= 1
      if n == 0:
        raise err
      logger.warning(f"{coro} failed, trying again in {backoff}s...")
      await asyncio.sleep(backoff)
      backoff *= 2
