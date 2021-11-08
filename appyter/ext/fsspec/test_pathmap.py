import multiprocessing as mp
mp.set_start_method('spawn', True)

import tempfile
import contextlib
from pathlib import Path
from appyter.ext.asyncio.sync_contextmanager import sync_contextmanager

import appyter.ext.fsspec
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.fsspec.fuse import fs_mount

def assert_eq(a, b): assert a == b, f"{repr(a)} != {repr(b)}"

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

def test_file_pathmap_chroot():
  with _test_ctx() as tmpdir:
    # instantiate filesystem & check that it works
    with url_to_chroot_fs(str(tmpdir), pathmap={'E': str(tmpdir/'e')}) as fs:
      assert_eq(frozenset(fs.glob('**')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e', 'E']))
      assert_eq(fs.cat('a/b/c'), b'C')
      assert_eq(fs.cat('a/d'), b'D')
      assert_eq(fs.cat('e'), b'E')
      assert_eq(fs.cat('E'), b'E')

def test_file_pathmap_chroot_fuse():
  with _test_ctx() as tmpdir:
    with sync_contextmanager(fs_mount(str(tmpdir), pathmap={'E': str(tmpdir/'e')})) as fs:
      assert_eq(frozenset(str(p.relative_to(fs)) for p in fs.rglob('*')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e', 'E']))
      assert_eq((fs/'a'/'b'/'c').open('rb').read(), b'C')
      assert_eq((fs/'a'/'d').open('rb').read(), b'D')
      assert_eq((fs/'e').open('rb').read(), b'E')
      assert_eq((fs/'E').open('rb').read(), b'E')
      with (fs/'E').open('a') as fw:
        fw.write('!')
      assert_eq((fs/'E').open('rb').read(), b'E!')
      with (fs/'E').open('w') as fw:
        fw.write('E')
      assert_eq((fs/'E').open('rb').read(), b'E')

def _http_serve(directory, port=8888):
  ''' Serve a simple static listing of the given directory on the specified port
  '''
  from aiohttp import web
  app = web.Application()
  app.add_routes([web.static('/subdir', str(directory), show_index=True)])
  return web.run_app(app, port=port)

async def _http_connect(url):
  ''' Successfully connect to and resolve a url
  '''
  import aiohttp
  async with aiohttp.ClientSession() as session:
    async with session.get(url) as response:
      return await response.text()

@contextlib.contextmanager
def _http_serve_ctx(directory, port=8888):
  ''' Context for _http_serve, ensuring server is ready before proceeding
  '''
  import os
  import signal
  from multiprocessing import Process
  from appyter.ext.asyncio.try_n_times import try_n_times
  from appyter.ext.asyncio.sync_coro import sync_coro
  proc = Process(
    target=_http_serve, args=(directory, port)
  )
  proc.start()
  try:
    sync_coro(try_n_times(3, _http_connect, f"http://localhost:{port}"))
    yield
  finally:
    if proc.pid:
      os.kill(proc.pid, signal.SIGINT)

def test_http_pathmap_chroot():
  ''' Serve the test directory over http and ensure chroot_fs still works using the webserver
  '''
  port = 8888
  with _test_ctx() as tmpdir:
    with _http_serve_ctx(str(tmpdir), port):
      # instantiate filesystem & check that it works
      with url_to_chroot_fs(f"http://localhost:{port}/subdir/", pathmap={'E': f'http://localhost:{port}/subdir/e'}) as fs:
        assert_eq(fs.cat('a/b/c'), b'C')
        assert_eq(fs.cat('a/d'), b'D')
        assert_eq(fs.cat('e'), b'E')
        assert_eq(fs.cat('E'), b'E')
