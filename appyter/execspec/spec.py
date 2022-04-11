from appyter.ext.urllib import URI
from appyter.ext.asyncio.helpers import ensure_sync

class AbstractExecutor:
  protocol = None

  def __init__(self, url=None, **kwargs) -> None:
    self.url = url
    self.executor_options = kwargs
  
  @classmethod
  def parse(cls, url) -> dict:
    url = URI(url)
    return dict(url=str(url.with_fragment(None)), **url.fragment_query_ex)

  async def __aenter__(self):
    return self

  def __enter__(self):
    return ensure_sync(self.__aenter__())

  async def __aexit__(self, type, value, traceback):
    pass

  def __exit__(self, type, value, traceback):
    return ensure_sync(self.__aexit__(type, value, traceback))

  async def _run(self, **job):
    raise NotImplementedError

  def run(self, **job):
    return ensure_sync(self._run(**job))
