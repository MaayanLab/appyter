import contextlib
import traceback
import logging

logger = logging.getLogger(__name__)

from pathlib import PurePosixPath
from fsspec import filesystem, AbstractFileSystem
from appyter.ext.pathlib.chroot import ChrootPurePosixPath

class ChrootFileSystem(AbstractFileSystem):
  ''' chroot: update root and disallow access beyond chroot, only works on directories.
  '''
  root_marker = '/'
  protocol = 'chroot'

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

  def __resolve_path(self, path):
    resolved_path = self.fs.root_marker + str((ChrootPurePosixPath('/'+self.storage_options['fo'].lstrip('/')) / ('/'+path.lstrip('/'))).realpath()).lstrip('/')
    return resolved_path

  def __unresolve_path(self, path):
    unresolve_path = self.root_marker + str(PurePosixPath('/'+path.lstrip('/')).relative_to('/'+self.storage_options['fo'].lstrip('/')))
    return unresolve_path

  @contextlib.contextmanager
  def __masquerade_os_error(self):
    try:
      yield
    except OSError as e:
      logger.error(traceback.format_exc())
      filename = self.__unresolve_path(e.filename) if e.filename else None
      winerror = getattr(e, 'winerror', None)
      filename2 = self.__unresolve_path(e.filename2) if e.filename2 else None
      raise OSError(e.errno, e.strerror, filename, winerror, filename2) from None
    except Exception as e:
      logger.error(traceback.format_exc())
      raise Exception(f"{e.__class__.__name__} occurred, details have been hidden for security reasons")

  def __enter__(self):
    if getattr(self.fs, '__enter__', None) is not None:
      with self.__masquerade_os_error():
        self.fs.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.fs, '__exit__', None) is not None:
      with self.__masquerade_os_error():
        self.fs.__exit__(type, value, traceback)

  def mkdir(self, path, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.mkdir(self.__resolve_path(path), **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    with self.__masquerade_os_error():
      return self.fs.rm(self.__resolve_path(path), recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.copy(self.__resolve_path(path1), self.__resolve_path(path2), recursive=recursive, on_error=on_error, **kwargs)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.mv(self.__resolve_path(path1), self.__resolve_path(path2), recursive=recursive, maxdepth=maxdepth, **kwargs)

  def info(self, path, **kwargs):
    with self.__masquerade_os_error():
      info = self.fs.info(self.__resolve_path(path), **kwargs)
      return dict(info, name=self.__unresolve_path(info['name']))

  def ls(self, path, detail=True, **kwargs):
    results = []
    with self.__masquerade_os_error():
      for f in self.fs.ls(self.__resolve_path(path), detail=detail, **kwargs):
        if detail:
          f = dict(f, name=self.__unresolve_path(f['name']))
          results.append(f)
        else:
          results.append(self.__unresolve_path(f))
    return results

  def _open(self, path, mode="rb", block_size=None, cache_options=None, **kwargs):
    with self.__masquerade_os_error():
      return self.fs._open(self.__resolve_path(path), mode=mode, block_size=block_size, cache_options=cache_options, **kwargs)
