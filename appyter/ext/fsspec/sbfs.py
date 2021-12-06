import sys
import tempfile
from subprocess import Popen
from pathlib import Path
from fsspec.spec import AbstractFileSystem
from appyter.ext.asyncio.try_n_times import try_n_times

from appyter.ext.fsspec.chroot import ChrootFileSystem
from appyter.ext.pathlib.assertions import assert_mounted, assert_unmounted
from appyter.ext.pathlib.chroot import ChrootPurePosixPath

class SBFSFileSystem(AbstractFileSystem):
  def __init__(self, *args, api_endpoint='', auth_token='', **storage_options):
    super().__init__(*args, api_endpoint=api_endpoint, auth_token=auth_token, **storage_options)

  def __enter__(self):
    ''' Mount sbfs into temporary directory
    '''
    self._tmpdir = Path(tempfile.mkdtemp())
    self._proc = Popen([
      'sbfs',
      f"--api-endpoint={self.storage_options['api_endpoint']}",
      f"--auth-token={self.storage_options['auth_token']}",
      'mount',
      '--foreground',
      str(self._tmpdir),
    ], stderr=sys.stderr, stdout=sys.stdout)
    try_n_times(3, assert_mounted, self._tmpdir)
    self.fs = ChrootFileSystem(
      target_protocol='file',
      fo=str(self._tmpdir),
      target_options=dict(auto_mkdir=True),
    )
    return self
  
  def __exit__(self, exc_type, exc_value, traceback):
    ''' Cleanly exit sbfs & cleanup temporary directory
    '''
    if self._proc.pid:
      import os, signal
      os.kill(self._proc.pid, signal.SIGINT)
      self._proc.wait()
    try_n_times(3, assert_unmounted, self._tmpdir)
    self._tmpdir.rmdir()
  
  def _poll(self):
    ''' Ensure sbfs is still running
    '''
    if getattr(self, '_proc', None) is None:
      raise Exception('Contextmanager is required for sbfs')
    if self._proc.poll() is not None:
      raise Exception('sbfs exited')
  
  def _block_info(self, path):
    ''' Report permission error if trying to access `.info`
    '''
    if str(ChrootPurePosixPath('/') / path) == '.info':
      raise PermissionError
  
  def mkdir(self, path, **kwargs):
    self._poll()
    self._block_info(path)
    return self.fs.mkdir(path, **kwargs)

  def makedirs(self, path, exist_ok=False):
    self._poll()
    self._block_info(path)
    return self.fs.makedirs(path, exist_ok=exist_ok)

  def rmdir(self, path):
    self._poll()
    self._block_info(path)
    return self.fs.rmdir(path)

  def rm(self, path, recursive=False, maxdepth=None):
    self._poll()
    self._block_info(path)
    return self.fs.rm(path, recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    self._poll()
    self._block_info(path1)
    self._block_info(path2)
    return self.fs.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    self._poll()
    self._block_info(path1)
    self._block_info(path2)
    return self.fs.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)

  def exists(self, path, **kwargs):
    self._poll()
    self._block_info(path)
    return self.fs.exists(path, **kwargs)

  def info(self, path, **kwargs):
    self._poll()
    self._block_info(path)
    return self.fs.info(path, **kwargs)

  def ls(self, path, detail=True, **kwargs):
    ''' List all files except for special `.info` file
    '''
    self._poll()
    if detail:
      return [
        p
        for p in self.fs.ls(path, detail=True, **kwargs)
        if p['name'] != '.info'
      ]
    else:
      return [
        p
        for p in self.fs.ls(path, detail=False, **kwargs)
        if p != '.info'
      ]

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    self._poll()
    self._block_info(path)
    return self.fs._open(path, mode=mode, block_size=block_size, autocommit=autocommit, cache_options=cache_options, **kwargs)
