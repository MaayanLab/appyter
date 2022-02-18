import asyncio
import itertools
import logging
logger = logging.getLogger(__name__)

class PriorityQueuedEmitMixin:
  ''' A mixin for queuing `emit` calls to get triggered sequentially when `emit_enabled` event is set
  '''
  async def __aenter__(self):
    self._emit_enabled = asyncio.Event()
    self._emit_counter = iter(itertools.count())
    self._emit_queue = asyncio.PriorityQueue()
    self._emit_dispatcher_task = asyncio.create_task(self._emit_dispatcher())

  async def __aexit__(self, *args):
    try:
      self._emit_dispatcher_task.cancel()
      await self._emit_dispatcher_task
    except asyncio.CancelledError:
      pass

  async def _emit_dispatcher(self):
    while True:
      _, _, args, kwargs = await self._emit_queue.get()
      await self._emit_enabled.wait()
      try:
        await super().emit(*args, **{k:v for k,v in kwargs.items() if v})
      except asyncio.CancelledError:
        raise
      except:
        import traceback
        logger.error(traceback.format_exc())
      finally:
        self._emit_queue.task_done()

  async def emit(self, evt, data, priority=0, **kwargs):
    logger.debug('Priority queued emit')
    await self._emit_queue.put((
      priority, next(self._emit_counter), 
      (evt, data),
      kwargs,
    ))

  async def disconnect(self):
    logger.debug('Disconnecting...')
    if self._emit_enabled.is_set():
      logger.debug('Ensuring emit queue has been fully processed...')
      await self._emit_queue.join()
    logger.debug('Disconnect')
    try:
      self._emit_dispatcher_task.cancel()
      await self._emit_dispatcher_task
    except asyncio.CancelledError:
      pass
    await super().disconnect()
