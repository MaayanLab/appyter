import contextlib
from appyter.ext.asyncio.helpers import ensure_sync

def assert_eq(a, b): assert a == b, f"{repr(a)} != {repr(b)}"

@contextlib.contextmanager
def assert_exc(ExpectedException):
  try:
    yield
    assert False, f"Expected {ExpectedException}, got no error"
  except ExpectedException:
    assert True

@contextlib.asynccontextmanager
async def _http_serve(directory, port=8888):
  ''' Serve a simple static listing of the given directory on the specified port
  '''
  from aiohttp import web
  from appyter.ext.aiohttp import with_app_running
  app = web.Application()
  app.add_routes([web.static('/subdir', str(directory), show_index=True)])
  async with with_app_running(app, port=port):
    yield

async def _http_connect(url, ssl_verify=False):
  ''' Successfully connect to and resolve a url
  '''
  import aiohttp
  async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=ssl_verify)) as session:
    async with session.get(url) as response:
      return await response.text()

@ensure_sync
@contextlib.asynccontextmanager
async def http_serve_ctx(directory, port=8888):
  ''' Context for _http_serve, ensuring server is ready before proceeding
  '''
  from appyter.ext.asyncio.try_n_times import async_try_n_times
  async with _http_serve(directory, port):
    await async_try_n_times(3, _http_connect, f"http://localhost:{port}")
    yield
