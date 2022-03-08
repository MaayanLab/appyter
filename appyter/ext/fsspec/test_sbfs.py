import appyter.ext.multiprocessing

import os
import logging

import pytest
from appyter.ext.pytest import assert_eq
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

FSSPEC_URI = os.environ.get('FSSPEC_URI')

@pytest.mark.skipif(not FSSPEC_URI or 'sbfs://' not in FSSPEC_URI, reason='FSSPEC_URI with sbfs:// necessary to test sbfs')
def test_sbfs():
  import uuid
  import appyter.ext.fsspec
  from pathlib import PurePosixPath
  from appyter.ext.fsspec.core import url_to_fs_ex
  fs, fs_path = url_to_fs_ex(FSSPEC_URI)
  logging.debug(f"{fs=}")
  path = PurePosixPath(fs_path) / f"appyter-test-{str(uuid.uuid4())}"
  logging.debug(path)
  import time
  with fs as fs:
    try:
      logging.debug(fs.ls(''))
      fs.makedirs(fs_path, exist_ok=True)
      logging.debug(f"{fs.ls(fs_path)}")
      fs.makedirs(str(path), exist_ok=True)
      logging.debug(f"{fs.ls(str(path))}")
      with fs.open(str(path/'a'), 'wb') as fw:
        fw.write(b'A')
      with fs.open(str(path/'a'), 'rb') as fr:
        assert_eq(fr.read(), b'A')
      fs.makedirs(str(path/'b'))
      with fs.open(str(path/'b/c'), 'wb') as fw:
        fw.write(b'C')
      with fs.open(str(path/'b/c'), 'rb') as fr:
        assert_eq(fr.read(), b'C')
      with fs.open(str(path/'a'), 'wb') as fw:
        fw.write(b'a')
      assert_eq(fs.cat(str(path/'a')), b'a')
      assert_eq(frozenset(fs.glob(str(path/'**'))), frozenset([str(path/'a'), str(path/'b'), str(path/'b/c')]))
    finally:
      fs.rm(str(path), recursive=True)
