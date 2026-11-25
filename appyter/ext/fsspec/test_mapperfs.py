import appyter.ext.multiprocessing

import tempfile
import contextlib
from pathlib import Path

from appyter.ext.fsspec.mapperfs import MapperFileSystem

import pytest
from appyter.ext.pytest import assert_eq
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

@contextlib.contextmanager
def _test_ctx():
  with tempfile.TemporaryDirectory() as tmpdir:
    tmpdir = Path(tmpdir)
    (tmpdir/'a'/'b').mkdir(parents=True)
    with (tmpdir/'a'/'b'/'c').open('w') as fw:
      fw.write('C')
    with (tmpdir/'a'/'d').open('w') as fw:
      fw.write('D')
    with (tmpdir/'e').open('w') as fw:
      fw.write('E')
    yield tmpdir

def test_file_mapperfs():
  with _test_ctx() as tmpdir:
    with MapperFileSystem(pathmap={'a/b/c': str(tmpdir/'a'/'b'/'c'), 'E': str(tmpdir/'e')}) as fs:
      assert_eq(frozenset(fs.glob('**')), frozenset(['a', 'a/b', 'a/b/c', 'E']))
      assert_eq(fs.cat('a/b/c'), b'C')
      assert_eq(fs.cat('E'), b'E')

@contextlib.contextmanager
def _streaming_server(content, port=8891):
  ''' Serve `content` at any path as a chunked response (no Content-Length)
  '''
  from aiohttp import web
  from appyter.ext.aiohttp import with_app_running
  from appyter.ext.asyncio.helpers import ensure_sync
  async def handler(request):
    response = web.StreamResponse()
    response.enable_chunked_encoding()
    await response.prepare(request)
    for i in range(0, len(content), 7):
      await response.write(content[i:i+7])
    await response.write_eof()
    return response
  app = web.Application()
  app.add_routes([web.get('/{tail:.*}', handler)])
  with ensure_sync(with_app_running(app, port=port)):
    yield f"http://127.0.0.1:{port}"

def test_mapperfs_unknown_size_fuse():
  ''' files without a known size (e.g. streamed http responses) can still be mounted
  '''
  import os
  from appyter.ext.fsspec.core import url_to_chroot_fs
  content = b'gene set\tdescription\tA\tB\tC\n' * 20
  with _streaming_server(content) as url:
    with tempfile.TemporaryDirectory() as tmpdir:
      # `::` in the query string must not be treated as fsspec url chaining
      fs = url_to_chroot_fs(tmpdir, pathmap={'test.gmt': f"{url}/library?criteria=model::Gene,rma::options"})
      with fs as fs:
        with fs.mount(fuse=True) as mnt:
          assert_eq(os.stat(mnt/'test.gmt').st_size, len(content))
          assert_eq((mnt/'test.gmt').read_bytes(), content)
          assert_eq((mnt/'test.gmt').read_bytes(), content)
