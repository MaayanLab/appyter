import appyter.ext.multiprocessing

import tempfile
import contextlib
from pathlib import Path

import appyter.ext.fsspec
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.fsspec.fuse import fs_mount
from appyter.ext.asyncio.helpers import ensure_sync

import pytest
from appyter.ext.pytest import http_serve_ctx, assert_eq
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
    fs = url_to_chroot_fs(str(tmpdir), pathmap={'E': str(tmpdir/'e')})
    with fs.mount(fuse=True) as fs:
      assert_eq(frozenset(str(p.relative_to(fs)) for p in fs.rglob('*')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e', 'E']))
      assert_eq((fs/'a'/'b'/'c').open('rb').read(), b'C')
      assert_eq((fs/'a'/'d').open('rb').read(), b'D')
      assert_eq((fs/'e').open('rb').read(), b'E')
      assert_eq((fs/'E').open('rb').read(), b'E')
      # with (fs/'E').open('a') as fw:
      #   fw.write('!')
      # assert_eq((fs/'E').open('rb').read(), b'E!')
      with (fs/'E').open('w') as fw:
        fw.write('E!')
      assert_eq((fs/'E').open('rb').read(), b'E!')

def test_http_pathmap_chroot():
  ''' Serve the test directory over http and ensure chroot_fs still works using the webserver
  '''
  port = 8888
  with _test_ctx() as tmpdir:
    with http_serve_ctx(str(tmpdir), port):
      # instantiate filesystem & check that it works
      with url_to_chroot_fs(f"http://localhost:{port}/subdir/", pathmap={'E': f'http://localhost:{port}/subdir/e'}) as fs:
        assert_eq(fs.cat('a/b/c'), b'C')
        assert_eq(fs.cat('a/d'), b'D')
        assert_eq(fs.cat('e'), b'E')
        assert_eq(fs.cat('E'), b'E')
