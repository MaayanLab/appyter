import os
import contextlib
from pathlib import PurePath
from fsspec import AbstractFileSystem, filesystem
from appyter.ext.fsspec.spec.mountable import MountableAbstractFileSystem
from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem
from appyter.ext.pathlib import is_relative_to
from appyter.ext.tempfile import mktemp

import logging
logger = logging.getLogger(__name__)

class WriteCacheFileSystem(MountableAbstractFileSystem, ComposableAbstractFileSystem, AbstractFileSystem):
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
    self._local_cache = {}
    self._dir_cache = set()

  def __enter__(self):
    if getattr(self.fs, '__enter__', None) is not None:
      self.fs.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.fs, '__exit__', None) is not None:
      self.fs.__exit__(type, value, traceback)

  @contextlib.contextmanager
  def mount(self, path='', mount_dir=None, fuse=True, **kwargs):
    mount = self.fs.mount if getattr(self.fs, 'mount', None) is not None else super().mount
    with mount(path=path, mount_dir=mount_dir, fuse=fuse, **kwargs) as mount_dir:
      yield mount_dir

  def mkdir(self, path, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    try:
      self.fs.mkdir(path, **kwargs)
    except:
      raise
    else:
      self._dir_cache.add(path)

  def makedirs(self, path, exist_ok=False):
    path = self.fs.root_marker + path.lstrip('/')
    try:
      self.fs.makedirs(path, exist_ok=exist_ok)
    except:
      raise
    else:
      path_split = path.split('/')
      for i in range(1, len(path_split)+1):
        self._dir_cache.add('/'.join(path_split[:i]))

  def rmdir(self, path):
    path = self.fs.root_marker + path.lstrip('/')
    try:
      self.fs.rmdir(path)
    except:
      raise
    else:
      self._dir_cache.discard(path)

  def rm_file(self, path):
    path = self.fs.root_marker + path.lstrip('/')
    try:
      self.fs.rm_file(path)
    except:
      raise
    else:
      self._local_cache.discard(path)

  def rm(self, path, recursive=False, maxdepth=None):
    path = self.fs.root_marker + path.lstrip('/')
    try:
      self.fs.rm(path, recursive=recursive, maxdepth=maxdepth)
    except:
      raise
    else:
      if recursive:
        for d in list(self._dir_cache):
          if d.startswith(path):
            self._dir_cache.remove(d)

  def cat_file(self, path, start=None, end=None, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    try:
      return self.fs.cat_file(path, start=start, end=end, **kwargs)
    except KeyboardInterrupt:
      raise
    except:
      if path in self._local_cache:
        fh = self._local_cache[path]
        cur = fh.tell()
        fh.seek(start or 0)
        if end is None:
          contents = fh.read()
        else:
          contents = fh.read(end - (start or 0))
        fh.seek(cur)
        return contents
      else:
        raise

  def put_file(self, lpath, rpath, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    return self.fs.put_file(lpath, self._resolve_path(rpath), **kwargs)

  def get_file(self, rpath, lpath, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    return self.fs.get_file(self._resolve_path(rpath), lpath, **kwargs)

  def cp_file(self, path1, path2, **kwargs):
    path1 = self.fs.root_marker + path1.lstrip('/')
    path2 = self.fs.root_marker + path2.lstrip('/')
    return self.fs.cp_file(path1, path2, **kwargs)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    path1 = self.fs.root_marker + path1.lstrip('/')
    path2 = self.fs.root_marker + path2.lstrip('/')
    try:
      self.fs.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)
    except:
      raise
    else:
      if recursive:
        p1 = PurePath(path1)
        p2 = PurePath(path2)
        for d in list(self._dir_cache):
          p = PurePath(d)
          if is_relative_to(p, p1):
            self._dir_cache.add(str(p2 / p.relative_to(path1)))

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    path1 = self.fs.root_marker + path1.lstrip('/')
    path2 = self.fs.root_marker + path2.lstrip('/')
    try:
      self.fs.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)
    except:
      raise
    else:
      if recursive:
        p1 = PurePath(path1)
        p2 = PurePath(path2)
        for d in list(self._dir_cache):
          p = PurePath(d)
          if is_relative_to(p, p1):
            self._dir_cache.remove(d)
            self._dir_cache.add(str(p2 / p.relative_to(path1)))

  def exists(self, path, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    if path in self._local_cache or path in self._dir_cache:
      return True
    return self.fs.exists(path, **kwargs)

  def get_drs(self, path, **kwargs):
    return self.fs.get_drs(path, **kwargs)

  def info(self, path, **kwargs):
    path = self.fs.root_marker + path.lstrip('/')
    if path in self._local_cache:
      return self._local_cache[path]
    elif path in self._dir_cache:
      return {'type': 'directory', 'name': path}
    return self.fs.info(path, **kwargs)

  def ls(self, path, detail=False, **kwargs):
    # add local paths
    path = self.fs.root_marker + path.lstrip('/')
    logger.info(f'ls({path})')
    path_split = ('',) if path == self.fs.root_marker else tuple(path.split('/'))
    results = {}
    for local_file_path, f in self._local_cache.items():
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
      if path in self._local_cache:
        details = self._local_cache[path]
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
    fs._local_cache[path] = details if details else {'type': 'file', 'size': 0}
    fn = fn or mktemp()
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
    self.cleanup()

  def commit(self):
    self.fs.fs.put(self.fn, self.path)
    self.cleanup()

  def cleanup(self):
    os.remove(self.fn)
    if self.path in self.fs._local_cache:
      del self.fs._local_cache[self.path]

  def __getattr__(self, item):
    return getattr(self.fh, item)
