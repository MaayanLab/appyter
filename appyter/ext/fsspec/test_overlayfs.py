import appyter.ext.multiprocessing

import tempfile
import contextlib
from pathlib import Path
from fsspec.core import url_to_fs

import appyter.ext.fsspec
from appyter.ext.fsspec.overlayfs import OverlayFileSystem

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

def test_file_overlayfs():
  with _test_ctx() as lower_tmpdir:
    with tempfile.TemporaryDirectory() as upper_tmpdir:
      upper_tmpdir = Path(upper_tmpdir)
      assert_eq(frozenset(str(p.relative_to(lower_tmpdir)) for p in lower_tmpdir.rglob('*')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e']))
      lower_fs, _ = url_to_fs(f"chroot::{lower_tmpdir}")
      upper_fs, _ = url_to_fs(f"chroot::{upper_tmpdir}")
      with OverlayFileSystem(lower_fs=lower_fs, upper_fs=upper_fs) as fs:
        assert_eq(frozenset(fs.glob('**')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e']))
        fs.copy('e', 'E')
        fs.pipe('e', b'A')
        with fs.open('a/d', 'a') as fw:
          fw.write('!')
        assert_eq(fs.cat('a/d'), b'D!')
        with fs.open('a/d', 'a') as fw:
          fw.write('!')
        assert_eq(fs.cat('a/d'), b'D!!')
        assert_eq(fs.cat('e'), b'A')
        assert_eq(fs.cat('E'), b'E')
      assert_eq(frozenset(str(p.relative_to(upper_tmpdir)) for p in upper_tmpdir.rglob('*')), frozenset(['a', 'a/d', 'e', 'E']))
      assert_eq((upper_tmpdir/'e').open('rb').read(), b'A')
      assert_eq((upper_tmpdir/'E').open('rb').read(), b'E')
      assert_eq((upper_tmpdir/'a/d').open('rb').read(), b'D!!')
      assert_eq((lower_tmpdir/'a/d').open('rb').read(), b'D')
      assert_eq((lower_tmpdir/'e').open('rb').read(), b'E')
