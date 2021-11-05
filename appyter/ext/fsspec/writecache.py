import os
import tempfile
from fsspec import filesystem, AbstractFileSystem

import logging
logger = logging.getLogger(__name__)

class WriteCacheFileSystem(AbstractFileSystem):
  protocol = 'writecache'

  def __init__(self, target_protocol=None, target_options=None, fs=None, **kwargs):
    '''
    Parameters
    ----------
    target_protocol: str (optional)
      Target filesystem protocol. Provide either this or ``fs``.
    target_options: dict or None
      Passed to the instantiation of the FS, if fs is None.
    fs: filesystem instance
      The target filesystem to run against. Provide this or ``protocol``.
    '''
    super().__init__(**kwargs)
    if not (fs is None) ^ (target_protocol is None):
      raise ValueError(
          "Please provide one of filesystem instance (fs) or"
          " remote_protocol, not both"
      )
    self.kwargs = target_options or {}
    self.target_protocol = (
      target_protocol
      if isinstance(target_protocol, str)
      else (fs.protocol if isinstance(fs.protocol, str) else fs.protocol[0])
    )
    self.fs = fs if fs is not None else filesystem(target_protocol, **self.kwargs)
    self._local_files = {}

  def __enter__(self):
    if getattr(self.fs, '__enter__', None) is not None:
      self.fs.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.fs, '__exit__', None) is not None:
      self.fs.__exit__(type, value, traceback)

  def mkdir(self, path, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    return self.fs.mkdir(path, **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    path = self.fs.root_marker + path.lstrip('/')
    return self.fs.rm(path, recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    path1 = self.fs.root_marker + path1.lstrip('/')
    path2 = self.fs.root_marker + path2.lstrip('/')
    return self.fs.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    path1 = self.fs.root_marker + path1.lstrip('/')
    path2 = self.fs.root_marker + path2.lstrip('/')
    return self.fs.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)

  def exists(self, path, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    if path in self._local_files:
      return True
    return self.fs.exists(path, **kwargs)

  def info(self, path, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    if path in self._local_files:
      return self._local_files[path]
    return self.fs.info(path, **kwargs)

  def ls(self, path, detail=False, **kwargs):
    # add local paths
    path = self.fs.root_marker + path.lstrip('/')
    logger.info(f'ls({path})')
    path_split = ('',) if path == self.fs.root_marker else tuple(path.split('/'))
    results = {}
    for local_file_path, f in self._local_files.items():
      if tuple(local_file_path.split('/'))[:len(path_split)] == path_split:
        if detail:
          results[local_file_path] = f
        else:
          results[local_file_path] = local_file_path
    for f in self.fs.ls(path, detail=detail, **kwargs):
      if detail:
        results[f['name']] = f
      else:
        results[f] = f
    return list(results.values())

  def _open(self, path, mode='rb', **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    if 'r' not in mode or '+' in mode:
      if path in self._local_files:
        details = self._local_files[path]
      else:
        try:
          details = self.fs.info(path)
          if details['type'] == 'directory':
            raise IsADirectoryError(details['name'])
        except FileNotFoundError:
          details = None
      return LocalTempFile(self, path, mode=mode, details=details)
    return self.fs._open(path, mode=mode, **kwargs)

class LocalTempFile:
  """A temporary local file, which will be uploaded on commit"""

  def __init__(self, fs, path, fn=None, mode="wb", autocommit=True, seek=0, details=None):
    fs._local_files[path] = details if details else {'type': 'file', 'size': 0}
    fn = fn or tempfile.mktemp()
    self.mode = mode
    self.fn = fn
    # if the file exists on the remote and we need the contents, get them first
    if details and 'a' in mode or ('r' in mode and '+' in mode):
      fs.fs.get(path, fn)
    self.fh = open(fn, mode)
    if seek:
      self.fh.seek(seek)
    self.path = path
    self.fs = fs
    self.closed = False
    self.autocommit = autocommit

  def __reduce__(self):
    # always open in rb+ to allow continuing writing at a location
    return (
      LocalTempFile,
      (self.fs, self.path, self.fn, "rb+", self.autocommit, self.tell()),
    )

  def __enter__(self):
    return self.fh

  def __exit__(self, exc_type, exc_val, exc_tb):
    self.close()

  def close(self):
    self.fh.close()
    self.closed = True
    if self.autocommit:
      self.commit()

  def discard(self):
    self.fh.close()
    os.remove(self.fn)
    if self.path in self.fs._local_files:
      del self.fs._local_files[self.path]

  def commit(self):
    self.fs.fs.put(self.fn, self.path)
    if self.path in self.fs._local_files:
      del self.fs._local_files[self.path]

  def __getattr__(self, item):
    return getattr(self.fh, item)
