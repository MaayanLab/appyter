import logging
import asyncio
import traceback
import functools
import threading
import contextlib
from concurrent.futures import ThreadPoolExecutor
logger = logging.getLogger(__name__)

class SharedEventLoopThreadPoolExecutor(ThreadPoolExecutor):
  ''' This thread pool will initialize each thread with the same event loop.
  '''
  def __init__(self, *args, loop=None, initializer=None, **kwargs):
    initializer = functools.partial(self._initializer, initializer=initializer)
    super().__init__(*args, initializer=initializer, **kwargs)
    self.loop = loop or asyncio.get_event_loop()
  
  def _initializer(self, *args, initializer=None, **kwargs):
    logger.debug(f"Thread initializer {self.loop=}")
    asyncio.set_event_loop(self.loop)
    if initializer is not None:
      return initializer(*args, **kwargs)

class EventLoopThread(threading.Thread):
  ''' Keep the event loop running in this thread until `stop` is called.
  '''
  def __init__(self, loop=None):
    super().__init__()
    self.close = threading.Event()
    self.loop = loop or asyncio.get_event_loop()

  async def _run(self):
    logger.debug("Event loop started")
    try:
      await self.loop.run_in_executor(None, self.close.wait)
    except:
      logger.error(f"{traceback.format_exc()}")
    finally:
      logger.debug(f"Cancelling active tasks...")
      # we omit our own task since that would cause a deadlock
      #  and we cancel tasks in reverse which works well in python3.10,
      #  typically cancelling tasks launched last first
      tasks = reversed(list(asyncio.all_tasks() - {asyncio.current_task()}))
      for task in tasks:
        task.cancel()
        try:
          await task
        except asyncio.CancelledError:
          pass
        except:
          logger.error(traceback.format_exc())

  def run(self):
    try:
      self.loop.run_until_complete(self._run())
    finally:
      logger.debug(f"Event loop closed.")

  def stop(self):
    logger.debug("Stopping event loop...")
    self.close.set()
    self.join()

_LOOP = None

def new_event_loop():
  ''' Construct a new event loop with some custom extensions:
  - a dedicated thread to run the event loop
  - a thread pool executor that sets the event loop in spawned threads
  '''
  global _LOOP
  if _LOOP is not None:
    logger.warning('Event loop already exists')
    return _LOOP
  logger.debug(f"New event loop")
  try:
    import uvloop
    loop = uvloop.new_event_loop()
  except ImportError:
    logger.warning('Install uvloop for better performance')
    loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop_executor = SharedEventLoopThreadPoolExecutor(loop=loop)
  loop.set_default_executor(loop_executor)
  loop_thread = EventLoopThread(loop=loop)
  loop_thread.start()
  _loop_close = loop.close
  def loop_close(*args, **kwargs):
    global _LOOP
    logger.debug("Closing event loop...")
    loop_thread.stop()
    _LOOP = None
    return _loop_close(*args, **kwargs)
  setattr(loop, 'close', loop_close)
  setattr(loop, '_thread_id', loop_thread.ident)
  _LOOP = loop
  return _LOOP

def get_event_loop():
  ''' Get the same loop in different threads, create the loop if it doesn't exist
  '''
  global _LOOP
  if _LOOP is not None:
    return _LOOP
  else:
    return asyncio.get_running_loop()

@contextlib.contextmanager
def with_event_loop():
  loop = new_event_loop()
  try:
    yield loop
  finally:
    loop.close()
