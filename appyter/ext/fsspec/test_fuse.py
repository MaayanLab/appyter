import appyter.ext.multiprocessing

import tempfile
import contextlib
from pathlib import Path

import appyter.ext.fsspec
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.fsspec.fuse import fs_mount
from appyter.ext.asyncio.helpers import ensure_sync

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
    with (tmpdir/'a'/'b'/'c').open('w') as fw: fw.write('C')
    with (tmpdir/'a'/'d').open('w') as fw: fw.write('D')
    with (tmpdir/'e').open('w') as fw: fw.write('E')
    yield tmpdir

def test_file_chroot_fuse():
  with _test_ctx() as tmpdir:
    fs = url_to_chroot_fs(str(tmpdir), pathmap={'g': str(tmpdir/'e')}, cached=True)
    with ensure_sync(fs_mount(fs)) as fs:
      # reads work
      assert_eq(frozenset(str(p.relative_to(fs)) for p in fs.rglob('*')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e', 'g']))
      with (fs/'a'/'b'/'c').open('rb') as fr: assert_eq(fr.read(), b'C')
      with (fs/'a'/'d').open('rb') as fr: assert_eq(fr.read(), b'D')
      with (fs/'e').open('rb') as fr: assert_eq(fr.read(), b'E')
      # pathmap works
      with (fs/'g').open('rb') as fr: assert_eq(fr.read(), b'E')
      # writes work
      with (fs/'f').open('wb') as fw: fw.write(b'f')
      with (fs/'f').open('rb') as fr: assert_eq(fr.read(), b'f')
      # overwrites work
      with (fs/'f').open('wb') as fw: fw.write(b'F')
      with (fs/'f').open('rb') as fr: assert_eq(fr.read(), b'F')
      # and make it to the underlying store
      with (tmpdir/'f').open('rb') as fr: assert_eq(fr.read(), b'F')
      assert_eq(frozenset(str(p.relative_to(tmpdir)) for p in tmpdir.rglob('*')), frozenset(['a', 'a/b', 'a/b/c', 'a/d', 'e', 'f']))
