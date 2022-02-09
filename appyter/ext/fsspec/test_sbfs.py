import multiprocessing as mp
mp.set_start_method('spawn', True)

import pytest
import os

def assert_eq(a, b): assert a == b, f"{repr(a)} != {repr(b)}"

@pytest.mark.skipif(not os.environ.get('SBFS_URI'), reason='SBFS_URI necessary to test sbfs')
def test_sbfs():
  import uuid, time
  from pathlib import PurePosixPath
  from appyter.ext.fsspec.core import url_to_fs_ex
  sbfs_url = os.environ.get('SBFS_URI')
  fs, fs_path = url_to_fs_ex(sbfs_url)
  path = PurePosixPath(fs_path) / f"appyter-test-{str(uuid.uuid4())}"
  with fs as fs:
    try:
      fs.makedirs(str(path))
      with fs.open(str(path/'a'), 'wb') as fw:
        fw.write(b'A')
        fw.flush()
      # time.sleep(0.5)
      with fs.open(str(path/'a'), 'rb') as fr:
        assert_eq(fr.read(), b'A')
      # time.sleep(0.5)
      with fs.open(str(path/'b/c'), 'wb') as fw:
        fw.write(b'C')
        fw.flush()
      # time.sleep(0.5)
      with fs.open(str(path/'b/c'), 'rb') as fr:
        assert_eq(fr.read(), b'C')
      # time.sleep(0.5)
      with fs.open(str(path/'a'), 'wb') as fw:
        fw.write(b'a')
        fw.flush()
      # time.sleep(0.5)
      assert_eq(fs.cat(str(path/'a')), b'a')
      # time.sleep(0.5)
      assert_eq(frozenset(fs.glob(str(path/'**'))), frozenset([str(path/'a'), str(path/'b'), str(path/'b/c')]))
    finally:
      fs.rm(str(path), recursive=True)
