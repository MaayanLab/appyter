import contextlib
import traceback
import logging

from appyter.ext.urllib import join_slash

logger = logging.getLogger(__name__)

from pathlib import Path, PurePosixPath
from fsspec import AbstractFileSystem, filesystem
from appyter.ext.fsspec.spec import MountableAbstractFileSystem
from appyter.ext.pathlib.chroot import ChrootPurePosixPath

class ChrootFileSystem(MountableAbstractFileSystem, AbstractFileSystem):
  ''' chroot: update root and disallow access beyond chroot, only works on directories.
  '''
  root_marker = ''
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

  def _target_fo(self):
    if '://' in self.storage_options.get('fo', ''):
      target_fo_split = self.storage_options.get('fo','').split('/')
      # [scheme://base-path][/path-part?...]
      return '/'.join(target_fo_split[:3]), '/' + '/'.join(target_fo_split[3:])
    else:
      return '', self.storage_options.get('fo', '')

  def _resolve_path(self, path):
    target_fo_base, target_fo_path = self._target_fo()
    resolved_path = join_slash(*filter(None, (target_fo_base, str((ChrootPurePosixPath(target_fo_path) / path).realpath()))))
    if resolved_path == '.':
      resolved_path = ''
    if resolved_path.startswith('./'):
      resolved_path = resolved_path[2:]
    return resolved_path

  def _unresolve_path(self, path):
    target_fo_base, target_fo_path = self._target_fo()
    if not path.startswith(target_fo_base):
      raise FileNotFoundError(path)
    path = path[len(target_fo_base):]
    # ensure leading/trailing slash is the same
    if path.startswith('/') and not target_fo_path.startswith('/'):
      path = path.lstrip('/')
    elif not path.startswith('/') and target_fo_path.startswith('/'):
      path = '/' + path
    unresolve_path = str(PurePosixPath(path).relative_to(target_fo_path))
    return unresolve_path

  @contextlib.contextmanager
  def __masquerade_os_error(self, path=None):
    try:
      yield
    except FileNotFoundError:
      if path:
        raise FileNotFoundError(path)
      else:
        raise FileNotFoundError
    except PermissionError:
      if path:
        raise PermissionError(path)
      else:
        raise PermissionError
    except OSError as e:
      logger.error(traceback.format_exc())
      if e.errno:
        raise type(e)(e.errno, f'{e.__class__.__name__} occurred, details have been hidden for security reasons')
      else:
        raise Exception(f"{e.__class__.__name__} occurred, details have been hidden for security reasons")
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

  @contextlib.contextmanager
  def mount(self, mount_dir=None, fuse=True, **kwargs):
    logger.debug(f"{self=} mount {mount_dir=} {fuse=}")
    if not fuse and self.fs.protocol == 'file':
      yield Path(self.storage_options['fo'])
    elif getattr(self.fs, 'mount', None) is not None:
      with self.fs.mount(mount_dir=mount_dir, fuse=fuse, **kwargs) as mount_dir:
        yield mount_dir
    else:
      from appyter.ext.asyncio.helpers import ensure_sync
      from appyter.ext.fsspec.fuse import fs_mount
      _, target_fo_path = self._target_fo()
      with ensure_sync(fs_mount(
        f"chroot::{self.fs.protocol}://{target_fo_path}",
        mount_dir=mount_dir,
        **{ self.protocol: self.kwargs }
      )) as mount_dir:
        yield mount_dir

  def mkdir(self, path, **kwargs):
    with self.__masquerade_os_error(path=path):
      return self.fs.mkdir(self._resolve_path(path), **kwargs)

  def makedirs(self, path, exist_ok=False):
    with self.__masquerade_os_error(path=path):
      return self.fs.makedirs(self._resolve_path(path), exist_ok=exist_ok)

  def rmdir(self, path):
    with self.__masquerade_os_error(path=path):
      return self.fs.rmdir(self._resolve_path(path))

  def rm_file(self, path):
    with self.__masquerade_os_error(path=path):
      return self.fs.rm_file(self._resolve_path(path))

  def rm(self, path, recursive=False, maxdepth=None):
    with self.__masquerade_os_error(path=path):
      return self.fs.rm(self._resolve_path(path), recursive=recursive, maxdepth=maxdepth)

  def cat_file(self, path, start=None, end=None, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.cat_file(self._resolve_path(path), start=start, end=end, **kwargs)

  def put_file(self, lpath, rpath, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.put_file(lpath, self._resolve_path(rpath), **kwargs)

  def get_file(self, rpath, lpath, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.get_file(self._resolve_path(rpath), lpath, **kwargs)

  def cp_file(self, path1, path2, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.cp_file(self._resolve_path(path1), self._resolve_path(path2), **kwargs)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.copy(self._resolve_path(path1), self._resolve_path(path2), recursive=recursive, on_error=on_error, **kwargs)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    with self.__masquerade_os_error():
      return self.fs.mv(self._resolve_path(path1), self._resolve_path(path2), recursive=recursive, maxdepth=maxdepth, **kwargs)

  def exists(self, path, **kwargs):
    with self.__masquerade_os_error(path=path):
      return self.fs.exists(self._resolve_path(path), **kwargs)

  def info(self, path, **kwargs):
    with self.__masquerade_os_error(path=path):
      info = self.fs.info(self._resolve_path(path), **kwargs)
      return dict(info, name=self._unresolve_path(info['name']))

  def ls(self, path, detail=True, **kwargs):
    logger.debug(f"ls({path}) => fs.ls({self._resolve_path(path)})")
    results = []
    with self.__masquerade_os_error(path=path):
      for f in self.fs.ls(self._resolve_path(path), detail=detail, **kwargs):
        if detail:
          f = dict(f, name=self._unresolve_path(f['name']))
          results.append(f)
        else:
          results.append(self._unresolve_path(f))
    return results

  def _open(self, path, mode="rb", block_size=None, cache_options=None, **kwargs):
    with self.__masquerade_os_error(path=path):
      return self.fs._open(self._resolve_path(path), mode=mode, block_size=block_size, cache_options=cache_options, **kwargs)
