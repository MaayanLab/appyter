import appyter.ext.multiprocessing

import os
import uuid
import logging

import pytest
from appyter.ext.pytest import assert_eq
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

FSSPEC_URI = os.environ.get('FSSPEC_URI', f"file:///tmp/{str(uuid.uuid4())}")

@pytest.mark.skipif('memory://' in FSSPEC_URI, reason='in-memory store pre-init wont work with fuse in separate process')
def test_fuse_mount():
  from appyter.ext.fsspec.core import url_to_chroot_fs
  fs = url_to_chroot_fs(FSSPEC_URI)
  with fs as fs:
    try:
      fs.makedirs('', exist_ok=True)
      fs.pipe('test', b'Hello World!')
      with fs.mount(fuse=True) as mnt_dir:
        assert mnt_dir.is_mount(), 'Expected mount, got directory'
        logging.debug(f"{mnt_dir=}")
        assert_eq(
          frozenset({
            (p.name, p.open('rb').read())
            for p in mnt_dir.rglob('*') if p.is_file()
          }),
          frozenset({('test', b'Hello World!')}),
        )
        (mnt_dir/'hi').mkdir(exist_ok=True)
        (mnt_dir/'hi/world').open('w').write('test')
        assert_eq((mnt_dir/'hi/world').open('r').read(), 'test')
    finally:
      fs.rm('', recursive=True)

def test_fuseless_mount():
  from appyter.ext.fsspec.core import url_to_chroot_fs
  fs = url_to_chroot_fs(FSSPEC_URI)
  with fs as fs:
    try:
      fs.makedirs('', exist_ok=True)
      fs.pipe('test', b'Hello World!')
      with fs.mount(fuse=False) as mnt_dir:
        assert not mnt_dir.is_mount(), 'Expected directory, got mount'
        logging.debug(f"{mnt_dir=}")
        assert_eq(
          frozenset({
            (p.name, p.open('rb').read())
            for p in mnt_dir.rglob('*') if p.is_file()
          }),
          frozenset({('test', b'Hello World!')}),
        )
    finally:
      fs.rm('', recursive=True)
