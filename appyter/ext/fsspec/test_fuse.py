import multiprocessing as mp

from appyter.ext.asyncio.helpers import ensure_sync
mp.set_start_method('spawn', True)

import tempfile
import contextlib
from pathlib import Path

import appyter.ext.fsspec
from appyter.ext.fsspec.fuse import fs_mount

import pytest
@pytest.fixture(scope="session", autouse=True)
def setup():
  from appyter.ext.asyncio.event_loop import new_event_loop
  loop = new_event_loop()
  yield
  loop.close()

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

def test_file_chroot_fuse():
  with _test_ctx() as tmpdir:
    with ensure_sync(fs_mount(
      str(tmpdir),
      pathmap={'g': str(tmpdir/'e')},
      cached=True,
    )) as fs:
      # reads work
      assert_eq(frozenset(str(p.relative_to(fs)) for p in fs.rglob('*')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e', 'g']))
      assert_eq((fs/'a'/'b'/'c').open('rb').read(), b'C')
      assert_eq((fs/'a'/'d').open('rb').read(), b'D')
      assert_eq((fs/'e').open('rb').read(), b'E')
      # pathmap works
      assert_eq((fs/'g').open('rb').read(), b'E')
      # writes work
      with (fs / 'f').open('wb') as fw:
        fw.write(b'f')
      assert_eq((fs/'f').open('rb').read(), b'f')
      # overwrites work
      with (fs / 'f').open('wb') as fw:
        fw.write(b'F')
      assert_eq((fs/'f').open('rb').read(), b'F')
      # and make it to the underlying store
      assert_eq((tmpdir/'f').open('rb').read(), b'F')
