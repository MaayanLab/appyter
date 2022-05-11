import typing as t
import contextlib
import appyter.ext.fsspec
from appyter.ext.fsspec.core import url_to_fs_ex

import pytest
from appyter.ext.asyncio.helpers import ensure_sync
from appyter.ext.pytest import assert_eq
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

@contextlib.asynccontextmanager
async def _drs_serve(port=8888):
  import re
  import aiohttp.web
  import datetime as dt
  from appyter import __version__
  from appyter.ext.aiohttp import with_app_running
  from appyter.ext.cryptography import adhoc_ssl_context
  app = aiohttp.web.Application()
  routes = aiohttp.web.RouteTableDef()
  @routes.get('/ga4gh/drs/v1/service-info')
  async def drs_service_info(request: aiohttp.web.Request):
    return aiohttp.web.json_response({
      'id': f"cloud.maayanlab.appyter",
      'name': 'Appyter',
      'type': {
        'group': 'cloud.maayanlab.appyter',
        'artifact': 'drs',
        'version': '1.0.0',
      },
      'organization': {
        'name': 'MaayanLab',
        'url': 'https://maayanlab.cloud',
      },
      'version': __version__,
    })
  @routes.get('/ga4gh/drs/v1/objects/{file_id}')
  async def drs_object(request: aiohttp.web.Request):
    file_id = request.match_info['file_id']
    if file_id == '12345':
      return aiohttp.web.json_response({
        'id': file_id,
        'self_uri': f"{re.sub(r'^https?://', 'drs://', str(request.url.origin()))}/{file_id}",
        'access_methods': [
          {
            'access_id': 'primary',
            'type': 'https',
          },
        ],
        'checksums': [
          {
            'type': 'sha-1',
            'checksum': file_id,
          },
        ],
        'created_time': dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
        'size': 1,
      })
    else:
      raise aiohttp.web.HTTPNotFound()
  @routes.get('/ga4gh/drs/v1/objects/{file_id}/access/{access_id}')
  async def drs_object_access(request: aiohttp.web.Request):
    file_id = request.match_info['file_id']
    access_id = request.match_info['access_id']
    if access_id == 'primary' and file_id == '12345':
      return aiohttp.web.json_response({ 'url': f"{str(request.url.origin())}/ga4gh/drs/v1/objects/{file_id}/fetch" })
    else:
      raise aiohttp.web.HTTPNotFound()
  @routes.get('/ga4gh/drs/v1/objects/{file_id}/fetch')
  async def drs_object_fetch(request: aiohttp.web.Request):
    file_id = request.match_info['file_id']
    if file_id == '12345':
      return aiohttp.web.Response(body=b'A')
    else:
      raise aiohttp.web.HTTPNotFound()
  app.add_routes(routes)
  async with adhoc_ssl_context(cn=f"localhost:{port}") as ssl_context:
    async with with_app_running(app, port=port, ssl_context=ssl_context):
      yield

@ensure_sync
@contextlib.asynccontextmanager
async def drs_serve_ctx(port=8888):
  ''' Context for _drs_serve, ensuring server is ready before proceeding
  '''
  from appyter.ext.pytest import _http_connect
  from appyter.ext.asyncio.try_n_times import async_try_n_times
  async with _drs_serve(port):
    await async_try_n_times(3, _http_connect, f"https://localhost:{port}/ga4gh/drs/v1/service-info")
    yield

def test_drs():
  ''' Serve the test directory over http and ensure chroot_fs still works using the webserver
  '''
  port = 8888
  with drs_serve_ctx(port):
    fs, fo = url_to_fs_ex(f"drs://localhost:{port}/12345", ssl_verify=False)
    with fs as fs:
      with fs.open(fo, 'rb') as fr:
        assert_eq(fr.read(), b'A')
