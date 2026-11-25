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
  # writing through fuse requires the write cache for remote stores (as nbexecute does)
  fs = url_to_chroot_fs(FSSPEC_URI, cached=True)
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
        # seek works
        with (mnt_dir/'bye').open('w+') as fw:
          fw.write('hi!')
          fw.seek(0)
          fw.write('H')
        assert_eq((mnt_dir/'bye').open('r').read(), 'Hi!')
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

def test_fuseless_mount_copy_back():
  from appyter.ext.fsspec.core import url_to_chroot_fs
  fs = url_to_chroot_fs(FSSPEC_URI)
  with fs as fs:
    try:
      fs.makedirs('', exist_ok=True)
      fs.pipe('keep', b'keep')
      fs.pipe('modify', b'old')
      fs.pipe('delete', b'delete')
      with fs.mount(fuse=False) as mnt_dir:
        (mnt_dir/'modify').write_bytes(b'new')
        (mnt_dir/'delete').unlink()
        (mnt_dir/'sub'/'dir').mkdir(parents=True)
        (mnt_dir/'sub'/'dir'/'created').write_bytes(b'created')
      assert_eq(fs.cat('keep'), b'keep')
      assert_eq(fs.cat('modify'), b'new')
      assert_eq(fs.exists('delete'), False)
      assert_eq(fs.cat('sub/dir/created'), b'created')
    finally:
      fs.rm('', recursive=True)

def test_fuseless_overlay_copy_back(tmp_path):
  from appyter.ext.fsspec.core import url_to_chroot_fs
  (tmp_path/'input.txt').write_bytes(b'input')
  (tmp_path/'shadowed.txt').write_bytes(b'lower')
  (tmp_path/'edited.txt').write_bytes(b'unedited')
  fs = url_to_chroot_fs(FSSPEC_URI, pathmap={
    'input.txt': str(tmp_path/'input.txt'),
    'shadowed.txt': str(tmp_path/'shadowed.txt'),
    'edited.txt': str(tmp_path/'edited.txt'),
  })
  with fs as fs:
    try:
      fs.makedirs('', exist_ok=True)
      fs.pipe('shadowed.txt', b'upper')
      with fs.mount(fuse=False) as mnt_dir:
        # upper takes precedence, lower is visible
        assert_eq((mnt_dir/'shadowed.txt').read_bytes(), b'upper')
        assert_eq((mnt_dir/'input.txt').read_bytes(), b'input')
        (mnt_dir/'output.txt').write_bytes(b'output')
        (mnt_dir/'edited.txt').write_bytes(b'edited')
      # only the upper layer is written to, inputs aren't duplicated unless they were modified
      upper = url_to_chroot_fs(FSSPEC_URI)
      assert_eq(upper.cat('output.txt'), b'output')
      assert_eq(upper.cat('shadowed.txt'), b'upper')
      assert_eq(upper.cat('edited.txt'), b'edited')
      assert_eq(upper.exists('input.txt'), False)
      # the lower layer is untouched
      assert_eq((tmp_path/'edited.txt').read_bytes(), b'unedited')
    finally:
      fs.rm('', recursive=True)
