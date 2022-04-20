import logging
logger = logging.getLogger(__name__)

class ForwardingMixin:
  ''' A mixin for converting `to=` messages on the client to `forward` events to be handled by the server
  '''
  async def emit(self, evt, data, to=None, priority=0, **kwargs):
    if to is not None:
      logger.debug(f"Message forwarding {evt} to {to}")
      return await super().emit('forward', dict(event=evt, data=data, to=to, priority=priority))
    else:
      return await super().emit(evt, data, priority=priority)
