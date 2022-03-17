from appyter.ext.urllib import parse_qs
from appyter.ext.asyncio.helpers import ensure_sync

class AbstractExecutor:
  protocol = None

  def __init__(self, url=None, **kwargs) -> None:
    self.url = url
    self.executor_options = kwargs
  
  @classmethod
  def parse(cls, url) -> dict:
    url, _, qs = url.partition('?')
    opts = parse_qs(qs)
    return dict(url=url, **opts)

  async def __aenter__(self):
    return self
  __enter__ = ensure_sync(__aenter__)

  async def __aexit__(self, type, value, traceback):
    pass
  __exit__ = ensure_sync(__aexit__)

  async def _run(self, **job):
    raise NotImplementedError
  run = ensure_sync(_run)
