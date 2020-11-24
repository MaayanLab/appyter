import asyncio
import itertools
import logging
logger = logging.getLogger(__name__)

class PriorityQueuedEmitMixin:
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    try:
      loop = asyncio.get_event_loop()
    except:
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
    #
    self._emit_counter = iter(itertools.count())
    self._emit_queue = asyncio.PriorityQueue()
    self._emit_enabled = asyncio.Event()
    loop.create_task(self.emit_dispatcher())

  async def emit_dispatcher(self):
    while True:
      _, _, args, kwargs = await self._emit_queue.get()
      await self._emit_enabled.wait()
      try:
        await self.klass.emit(self, *args, **{k:v for k,v in kwargs.items() if v})
      except:
        import traceback
        logger.error(traceback.format_exc())
      self._emit_queue.task_done()

  async def _emit(self, evt, data, priority=0, **kwargs):
    await self._emit_queue.put((
      priority, next(self._emit_counter), 
      (evt, data),
      kwargs,
    ))

  async def emit(self, evt, data, priority=0, **kwargs):
    logger.debug('Priority queued emit')
    await self._emit(
      evt, data,
      priority=priority,
      **kwargs,
    )
