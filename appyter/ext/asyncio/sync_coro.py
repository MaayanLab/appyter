import asyncio
import threading

def sync_coro(coro):
  loop = asyncio.get_event_loop()
  res = loop.run_until_complete(coro)
  if threading.current_thread() is not threading.main_thread():
    loop.close()
  return res
