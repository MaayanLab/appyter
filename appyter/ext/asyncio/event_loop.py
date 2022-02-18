import logging
import asyncio
import functools
import threading
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
    logger.info(f"Thread initializer {self.loop=}")
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

  def run(self):
    self.loop.run_until_complete(
      self.loop.run_in_executor(None, self.close.wait)
    )

  def stop(self):
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
  logger.info(f"New Event Loop")
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop_executor = SharedEventLoopThreadPoolExecutor(loop=loop)
  loop.set_default_executor(loop_executor)
  loop_thread = EventLoopThread(loop=loop)
  loop_thread.start()
  _loop_close = loop.close
  def loop_close(*args, **kwargs):
    global _LOOP
    logger.info("Closing event loop...")
    loop_thread.stop()
    _LOOP = None
    return _loop_close(*args, **kwargs)
  setattr(loop, 'close', loop_close)
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
