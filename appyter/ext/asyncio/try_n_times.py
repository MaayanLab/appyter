import logging
logger = logging.getLogger(__name__)

async def try_n_times(n, coro, *args, **kwargs):
  import asyncio
  backoff = 1
  while n > 0:
    try:
      return await coro(*args, **kwargs)
    except Exception as err:
      n -= 1
      if n == 0:
        raise err
      logger.warn(f"{coro} failed, trying again in {backoff}s...")
      await asyncio.sleep(backoff)
      backoff *= 2
