import os
import uuid
import asyncio
import logging

FSSPEC_URI = os.environ.get('FSSPEC_URI', f"file:///tmp/{str(uuid.uuid4())}")

def test_fuseless_mount():
  from appyter.ext.fsspec.core import url_to_chroot_fs
  loop = asyncio.new_event_loop()
  fs = url_to_chroot_fs(FSSPEC_URI)
  with fs as fs:
    try:
      fs.makedirs('', exist_ok=True)
      fs.pipe('test', b'Hello World!')
      with fs.mount(fuse=False) as mnt_dir:
        logging.debug(f"{mnt_dir=} {({p: p.open('r').read() for p in mnt_dir.glob('*')})}")
    finally:
      fs.rm('', recursive=True)
