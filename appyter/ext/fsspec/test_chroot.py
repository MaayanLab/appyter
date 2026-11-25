import appyter.ext.multiprocessing

import tempfile
import contextlib
from pathlib import Path

import appyter.ext.fsspec
from appyter.ext.fsspec.core import url_to_chroot_fs

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

def test_file_chroot_in_chroot():
  with _test_ctx() as tmpdir:
    # instantiate filesystem & check that it works
    with url_to_chroot_fs(f"chroot::file://{str(tmpdir)}") as fs:
      assert_eq(frozenset(fs.glob('**')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e']))
      assert_eq(fs.cat('a/b/c'), b'C')
      assert_eq(fs.cat('a/d'), b'D')
      assert_eq(fs.cat('e'), b'E')

def test_file_chroot():
  with _test_ctx() as tmpdir:
    # instantiate filesystem & check that it works
    with url_to_chroot_fs(str(tmpdir)) as fs:
      assert_eq(frozenset(fs.glob('**')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e']))
      assert_eq(fs.cat('a/b/c'), b'C')
      assert_eq(fs.cat('a/d'), b'D')
      assert_eq(fs.cat('e'), b'E')

def test_http_chroot():
  ''' Serve the test directory over http and ensure chroot_fs still works using the webserver
  '''
  port = 8888
  with _test_ctx() as tmpdir:
    with http_serve_ctx(tmpdir, port):
      # instantiate filesystem & check that it works
      with url_to_chroot_fs(f"http://localhost:{port}/subdir/") as fs:
        assert_eq(fs.cat('a/b/c'), b'C')
        assert_eq(fs.cat('a/d'), b'D')
        assert_eq(fs.cat('e'), b'E')

def test_chroot_errors_hide_storage(tmp_path):
  ''' Errors must not reveal the underlying storage location (it may contain credentials),
  neither in the message nor in the traceback (via exception context)
  '''
  import traceback
  secret = 'SECRET-TOKEN-1234'
  root = tmp_path/secret
  (root/'dir').mkdir(parents=True)
  (root/'file').write_text('file')
  fs = url_to_chroot_fs(str(root))
  cases = [
    (FileNotFoundError, lambda: fs.cat('missing')),
    (FileNotFoundError, lambda: fs.info('missing')),
    (FileExistsError, lambda: fs.mkdir('file', create_parents=False)),
    (IsADirectoryError, lambda: fs.open('dir', 'rb').read()),
    (NotADirectoryError, lambda: fs.ls('file/sub')),
  ]
  for expected, fn in cases:
    try:
      fn()
    except Exception as e:
      formatted = ''.join(traceback.format_exception(e))
      assert secret not in str(e), f"{expected.__name__}: leaked in message: {e}"
      assert secret not in formatted, f"{expected.__name__}: leaked in traceback:\n{formatted}"
      assert e.__cause__ is None and e.__suppress_context__, f"{expected.__name__}: context not suppressed"
    else:
      assert False, f"expected an error for {expected.__name__}"
