from appyter.ext.urllib import parse_qs

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

  async def __aexit__(self, type, value, traceback):
    pass

  async def submit(self, job):
    raise NotImplementedError
  
  async def wait_for(self, id):
    raise NotImplementedError

  async def run(self, job):
    id = await self.submit(job)
    return await self.wait_for(id)
