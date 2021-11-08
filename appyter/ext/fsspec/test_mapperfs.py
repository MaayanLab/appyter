import multiprocessing as mp

from appyter.ext.fsspec.mapperfs import MapperFileSystem
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

def test_file_mapperfs():
  with _test_ctx() as tmpdir:
    with MapperFileSystem(pathmap={'a/b/c': str(tmpdir/'a'/'b'/'c'), 'E': str(tmpdir/'e')}) as fs:
      assert_eq(frozenset(fs.glob('**')), frozenset(['a', 'a/b', 'a/b/c', 'E']))
      assert_eq(fs.cat('a/b/c'), b'C')
      assert_eq(fs.cat('E'), b'E')
