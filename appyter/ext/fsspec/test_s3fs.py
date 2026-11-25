import appyter.ext.multiprocessing

import os
import uuid

import pytest
from appyter.ext.pytest import assert_eq, assert_exc
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

FSSPEC_URI = os.environ.get('FSSPEC_URI', '')
requires_s3 = pytest.mark.skipif(not FSSPEC_URI.startswith('s3://'), reason='FSSPEC_URI with s3:// necessary to test s3')

@pytest.fixture
def s3_fs():
  from appyter.ext.fsspec.core import url_to_chroot_fs
  from appyter.ext.urllib import URI
  # use a unique prefix under FSSPEC_URI
  uri = URI(FSSPEC_URI)
  fs = url_to_chroot_fs(str(uri.join(str(uuid.uuid4()))), cached=True)
  with fs as fs:
    fs.makedirs('', exist_ok=True)
    fs.pipe('file', b'file')
    try:
      yield fs
    finally:
      fs.rm('', recursive=True)

@requires_s3
def test_s3_mkdir(s3_fs):
  fs = s3_fs
  # making directories succeeds even though s3 has no directories
  fs.mkdir('newdir')
  assert_eq(fs.info('newdir')['type'], 'directory')
  fs.mkdir('newdir')
  fs.makedirs('a/b/c', exist_ok=True)
  fs.pipe('dir/x', b'x')
  fs.mkdir('dir')
  assert_eq(fs.info('dir')['type'], 'directory')
  # but a file is a file
  with assert_exc(FileExistsError):
    fs.mkdir('file')
  assert_eq(fs.info('file')['type'], 'file')

@requires_s3
@pytest.mark.parametrize('fuse', [True, False])
def test_s3_mkdir_mounted(s3_fs, fuse):
  fs = s3_fs
  fs.pipe('dir/x', b'x')
  with fs.mount(fuse=fuse) as mnt:
    (mnt/'newdir').mkdir()
    (mnt/'newdir'/'sub').mkdir(parents=True, exist_ok=True)
    (mnt/'dir').mkdir(exist_ok=True)
    (mnt/'newdir'/'sub'/'out').write_bytes(b'out')
    with assert_exc(FileExistsError):
      (mnt/'file').mkdir(exist_ok=True)
    assert (mnt/'file').is_file()
  assert_eq(fs.cat('newdir/sub/out'), b'out')
  assert_eq(fs.cat('file'), b'file')
