import asyncio
import logging
logger = logging.getLogger(__name__)

class EventEmitter:
  ''' Javascript-style event emitter
  '''
  def __init__(self):
    self._queues = {}
    self._consumers = {}
    self._listeners = {}
  #
  def _get_queue(self, event):
    if event not in self._queues:
      self._queues[event] = asyncio.Queue()
    return self._queues[event]
  #
  def _consumer_factory(self, event):
    async def _consumer():
      logger.debug(f"Starting consumer for {event}...")
      event_queue = self._get_queue(event)
      while True:
        evt = await event_queue.get()
        logger.debug(f"Calling listeners for {event}...")
        for listener in self._listeners.get(event, {}).values():
          asyncio.create_task(listener(**evt))
        event_queue.task_done()
    return _consumer
  #
  def _ensure_consumer(self, event):
    if event not in self._consumers:
      self._consumers[event] = asyncio.create_task(self._consumer_factory(event)())
    return self._consumers[event]
  #
  async def emit(self, event, **data):
    logger.debug(f"Emitting {event}: {data}")
    event_queue = self._get_queue(event)
    await event_queue.put(data)
  #
  def on(self, event):
    logger.debug(f"Attaching listener to {event}")
    def wrapper(listener):
      if event not in self._listeners:
        self._listeners[event] = {}
      self._listeners[event][listener] = listener
      self._ensure_consumer(event)
      return listener
    return wrapper
  #
  def off(self, event, listener):
    logger.debug(f"Detaching listener from {event}")
    del self._listeners[event][listener]
  #
  async def clear(self):
    logger.debug(f"Clearing...")
    for event in list(self._consumers):
      try:
        await self._queues[event].join()
        self._consumers[event].cancel()
        await self._consumers[event]
      except asyncio.CancelledError:
        pass
      finally:
        del self._consumers[event]
