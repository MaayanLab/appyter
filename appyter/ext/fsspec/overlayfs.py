import shutil
import contextlib
import logging

logger = logging.getLogger(__name__)

from fsspec import filesystem
from fsspec import AbstractFileSystem
from appyter.ext.fsspec.spec.mountable import MountableAbstractFileSystem
from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem
from appyter.ext.urllib import join_slash, parent_url

class OverlayFileSystem(MountableAbstractFileSystem, ComposableAbstractFileSystem, AbstractFileSystem):
  ''' OverlayFS implemented with fsspec
  '''
  root_marker = ''
  protocol = 'overlayfs'

  def __init__(self, lower_fs=None, lower_protocol=None, lower_options=dict(), upper_fs=None, upper_protocol=None, upper_options=dict(), **kwargs):
    '''
    Parameters
    ----------
    lower: str | fs | (protocol, options) initial
    upper: str | fs | (protocol, options) writes go here
    '''
    super().__init__(**kwargs)
    if not (lower_fs is None) ^ (lower_protocol is None):
      raise ValueError(
          "Please provide one of lower filesystem instance (lower_fs) or"
          " lower_protocol, not both"
      )
    if not (upper_fs is None) ^ (upper_protocol is None):
      raise ValueError(
          "Please provide one of upper filesystem instance (upper_fs) or"
          " upper_protocol, not both"
      )
    self.lower_fs = lower_fs if lower_fs is not None else filesystem(lower_protocol, **lower_options)
    self.upper_fs = upper_fs if upper_fs is not None else filesystem(upper_protocol, **upper_options)

  def __enter__(self):
    if getattr(self.lower_fs, '__enter__', None) is not None:
      self.lower_fs.__enter__()
    if getattr(self.upper_fs, '__enter__', None) is not None:
      self.upper_fs.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.upper_fs, '__exit__', None) is not None:
      self.upper_fs.__exit__(type, value, traceback)
    if getattr(self.lower_fs, '__exit__', None) is not None:
      self.lower_fs.__exit__(type, value, traceback)

  @contextlib.contextmanager
  def mount(self, path='', mount_dir=None, fuse=True, **kwargs):
    if not fuse:
      upper_mount = self.upper_fs.mount if getattr(self.upper_fs, 'mount', None) else super().mount
      lower_mount = self.lower_fs.mount if getattr(self.lower_fs, 'mount', None) else super().mount
      with upper_mount(path=path, mount_dir=mount_dir, fuse=fuse, **kwargs) as mount_dir:
        with lower_mount(path=path, mount_dir=mount_dir, fuse=fuse, **kwargs) as mount_dir:
          yield mount_dir
    else:
      with super().mount(path=path, mount_dir=mount_dir, fuse=fuse, **kwargs) as mount_dir:
        yield mount_dir

  def mkdir(self, path, **kwargs):
    return self.upper_fs.mkdir(path, **kwargs)
  
  def makedirs(self, path, exist_ok=False):
    return self.upper_fs.makedirs(path, exist_ok=exist_ok)

  def rmdir(self, path):
    return self.upper_fs.rmdir(path)

  def rm_file(self, path):
    return self.upper_fs.rm_file(path)

  def rm(self, path, recursive=False, maxdepth=None):
    return self.upper_fs.rm(path, recursive=recursive, maxdepth=maxdepth)

  def cat_file(self, path, start=None, end=None, **kwargs):
    if self.upper_fs.exists(path):
      return self.upper_fs.cat_file(path, start=start, end=end, **kwargs)
    elif self.lower_fs.exists(path):
      return self.lower_fs.cat_file(path, start=start, end=end, **kwargs)
    else:
      raise FileNotFoundError

  def put_file(self, lpath, rpath, **kwargs):
    return self.upper_fs.put(lpath, rpath, **kwargs)

  def get_file(self, rpath, lpath, **kwargs):
    if self.upper_fs.exists(rpath):
      return self.upper_fs.get_file(rpath, lpath, **kwargs)
    elif self.lower_fs.exists(rpath):
      return self.lower_fs.get_file(rpath, lpath, **kwargs)
    else:
      raise FileNotFoundError

  def cp_file(self, path1, path2, **kwargs):
    if self.upper_fs.exists(path1) or not self.lower_fs.exists(path1):
      return self.upper_fs.cp_file(path1, path2, **kwargs)
    else:
      with self.lower_fs.open(path1, 'rb') as fr:
        self.upper_fs.makedirs(parent_url(path2), exist_ok=True)
        with self.upper_fs.open(path2, 'wb') as fw:
          shutil.copyfileobj(fr, fw)

  def copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    if self.upper_fs.exists(path1) or not self.lower_fs.exists(path1):
      return self.upper_fs.copy(path1, path2, recursive=recursive, on_error=on_error, maxdepth=maxdepth, **kwargs)
    else:
      if self.lower_fs.isdir(path1) and recursive:
        for f1 in self.lower_fs.walk(path1, maxdepth=maxdepth):
          f_rel = f1.replace(path1, '')
          f2_rel = join_slash(path2, f_rel)
          with self.lower_fs.open(f1, 'rb') as fr:
            self.upper_fs.makedirs(parent_url(f2_rel), exist_ok=True)
            with self.upper_fs.open(f2_rel, 'wb') as fw:
              shutil.copyfileobj(fr, fw)
      else:
        with self.lower_fs.open(path1, 'rb') as fr:
          self.upper_fs.makedirs(parent_url(path2), exist_ok=True)
          with self.upper_fs.open(path2, 'wb') as fw:
            shutil.copyfileobj(fr, fw)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    if self.upper_fs.exists(path1):
      return self.upper_fs.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)
    else:
      raise PermissionError(path1)

  def exists(self, path, **kwargs):
    return self.upper_fs.exists(path, **kwargs) or self.lower_fs.exists(path, **kwargs)

  def get_drs(self, path, **kwargs):
    if self.upper_fs.exists(path) or not self.lower_fs.exists(path):
      return self.upper_fs.get_drs(path, **kwargs)
    else:
      return self.lower_fs.get_drs(path, **kwargs)

  def info(self, path, **kwargs):
    logger.debug(f"info({path})")
    if self.upper_fs.exists(path) or not self.lower_fs.exists(path):
      return self.upper_fs.info(path, **kwargs)
    else:
      return self.lower_fs.info(path, **kwargs)

  def ls(self, path, detail=False, **kwargs):
    logger.debug(f"ls({path})")
    results = {}
    lower_exists = self.lower_fs.exists(path)
    upper_exists = self.upper_fs.exists(path)
    if lower_exists:
      for info in self.lower_fs.ls(path, detail=detail, **kwargs):
        if detail:
          results[info['name']] = info
        else:
          results[info] = info
    if upper_exists or not lower_exists:
      for info in self.upper_fs.ls(path, detail=detail, **kwargs):
        if detail:
          results[info['name']] = info
        else:
          results[info] = info
    return list(results.values())

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    if 'r' not in mode:
      if 'w' in mode:
        pass
      elif not self.upper_fs.exists(path) and self.lower_fs.exists(path):
        with self.lower_fs.open(path, 'rb') as fr:
          self.upper_fs.makedirs(parent_url(path), exist_ok=True)
          with self.upper_fs.open(path, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
    elif self.upper_fs.exists(path):
      pass
    elif self.lower_fs.exists(path):
      # completely readonly and only exists in lower
      return self.lower_fs._open(
        path,
        mode=mode,
        block_size=block_size,
        autocommit=autocommit,
        cache_options=cache_options,
        **kwargs
      )
    #
    return self.upper_fs._open(
      path,
      mode=mode,
      block_size=block_size,
      autocommit=autocommit,
      cache_options=cache_options,
      **kwargs
    )
