import pathlib
import tempfile
import shutil
import contextlib

@contextlib.contextmanager
def tempdir(path=None):
  ''' A context for a temporary directory that may exist,
  if it doesn't we'll use mkdtemp. Also has a safety mechanism
  when dealing with mounts -- it will not rmtree if the directory
  is a mounted directory (since this might remove files unintentially).
  '''
  tempdir = pathlib.Path(tempfile.mkdtemp(prefix='appyter-tmp') if path is None else path)
  tempdir.mkdir(parents=True, exist_ok=True)
  try:
    yield tempdir
  finally:
    if path is None and not tempdir.is_mount() and tempdir.exists():
      shutil.rmtree(tempdir)

def mktemp(suffix='', prefix='appyter-tmp', dir=None):
  ''' Same as tempfile.mktemp but with appyter prefix
  '''
  return tempfile.mktemp(suffix=suffix, prefix=prefix, dir=dir)
