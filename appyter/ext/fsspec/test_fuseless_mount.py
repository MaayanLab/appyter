import os
import uuid
import logging

import pytest
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

FSSPEC_URI = os.environ.get('FSSPEC_URI', f"file:///tmp/{str(uuid.uuid4())}")

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
        logging.debug(f"{list(mnt_dir.glob('*'))=}")
        # logging.debug(f"{({p: p.open('rb').read() for p in mnt_dir.rglob('*') if p.is_file()})}")
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
        logging.debug(f"{mnt_dir=} {({p: p.open('r').read() for p in mnt_dir.rglob('*') if p.is_file()})}")
    finally:
      fs.rm('', recursive=True)
