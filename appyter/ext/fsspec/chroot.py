import contextlib
import traceback
import logging

from appyter.ext.urllib import join_slash

logger = logging.getLogger(__name__)

from pathlib import Path, PurePosixPath
from fsspec import AbstractFileSystem, filesystem
from appyter.ext.fsspec.spec.mountable import MountableAbstractFileSystem
from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem
from appyter.ext.pathlib.chroot import ChrootPurePosixPath

class ChrootFileSystem(MountableAbstractFileSystem, ComposableAbstractFileSystem, AbstractFileSystem):
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
    ''' Errors from the underlying filesystem may reveal the configured storage (e.g. a DATA_DIR
    with credentials) which must not leak into user-facing notebook executions. We re-raise them
    with at most the caller's (chroot-relative) path, and `from None` so that the original
    exception isn't attached as context (and thus shown in tracebacks). The full error is only
    logged server-side.
    '''
    try:
      yield
    except FileNotFoundError:
      if path:
        raise FileNotFoundError(path) from None
      else:
        raise FileNotFoundError from None
    except PermissionError:
      if path:
        raise PermissionError(path) from None
      else:
        raise PermissionError from None
    except (FileExistsError, IsADirectoryError, NotADirectoryError) as e:
      # preserve the type so callers can handle these
      if path:
        raise type(e)(path) from None
      else:
        raise type(e) from None
    except OSError as e:
      logger.error(traceback.format_exc())
      if e.errno:
        raise type(e)(e.errno, f'{e.__class__.__name__} occurred, details have been hidden for security reasons') from None
      else:
        raise Exception(f"{e.__class__.__name__} occurred, details have been hidden for security reasons") from None
    except Exception as e:
      logger.error(traceback.format_exc())
      raise Exception(f"{e.__class__.__name__} occurred, details have been hidden for security reasons") from None

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
  def mount(self, path='', mount_dir=None, fuse=True, passthrough=True, copy_back=True, overwrite=False, **kwargs):
    ''' Mount this filesystem on a local directory.

    fuse       use a fuse mount, otherwise files are copied into the directory
    copy_back  (without fuse) write new, modified & deleted files back to this filesystem on exit
    overwrite  (without fuse) replace files already present in mount_dir (e.g. from another layer)
    '''
    logger.debug(f"{self=} mount {mount_dir=} {fuse=}")
    with self.__masquerade_os_error(path=path):
      if passthrough and getattr(self.fs, 'mount', None) is not None:
        # try to use underlying fs mount
        with self.fs.mount(path=self._resolve_path(path), mount_dir=mount_dir, fuse=fuse, copy_back=copy_back, overwrite=overwrite, **kwargs) as mount_dir:
          yield mount_dir
      elif not fuse and mount_dir is None and 'file' in self.fs.protocol:
        # shortcut if we're talking about `file://` -- just use the actual directory
        yield Path(self._resolve_path(path))
      elif path:
        # just make another wrapper to deal with subpath mounting
        with ChrootFileSystem(fs=self.fs, fo=join_slash(self.storage_options.get('fo', ''), path)).mount(path='', mount_dir=mount_dir, fuse=fuse, passthrough=passthrough, copy_back=copy_back, overwrite=overwrite, **kwargs) as mount_dir:
          yield mount_dir
      elif fuse:
        # use fuse fs_mount
        from appyter.ext.asyncio.helpers import ensure_sync
        from appyter.ext.fsspec.fuse import fs_mount
        with ensure_sync(fs_mount(self, path, mount_dir=mount_dir)) as mount_dir:
          yield mount_dir
      else:
        # no fuse -- resort to copying files
        from appyter.ext.tempfile import tempdir
        with tempdir(mount_dir) as mount_dir:
          copied = self._copy_into(mount_dir, overwrite=overwrite)
          snapshot = _snapshot(mount_dir)
          _wait_for_newer_mtime(snapshot)
          logger.debug('Ready')
          try:
            yield mount_dir
          finally:
            if copy_back:
              self._copy_back(mount_dir, copied, snapshot)

  def _copy_into(self, mount_dir, overwrite=False):
    ''' Copy all files & directories into mount_dir, returning the relative paths we created
    '''
    import shutil
    logger.debug(f"copying files over...")
    copied = set()
    for f1_rel in self.glob('**', detail=True).values():
      f2_rel = mount_dir / f1_rel['name']
      f2_rel.parent.mkdir(parents=True, exist_ok=True)
      if f1_rel['type'] == 'file':
        if overwrite or not f2_rel.exists():
          logger.debug(f"copying {f1_rel['name']} to {str(f2_rel)}")
          # TODO: if we're backed by a normal filesystem, make a link
          with self.open(f1_rel['name'], 'rb') as fr:
            with f2_rel.open('wb') as fw:
              shutil.copyfileobj(fr, fw)
          copied.add(f1_rel['name'])
      elif f1_rel['type'] == 'directory':
        logger.debug(f"making directory {f1_rel['name']}")
        f2_rel.mkdir(exist_ok=True)
        copied.add(f1_rel['name'])
      else:
        raise NotImplementedError
    return copied

  def _copy_back(self, mount_dir, copied, snapshot):
    ''' Write changes made in mount_dir since `snapshot` back to this filesystem:
    new or modified files & directories are written, files & directories we copied in which
    no longer exist are removed. Files which came from elsewhere (e.g. another layer) are only
    written back if they were modified.
    '''
    import shutil
    logger.debug(f"copying changes back...")
    current = _snapshot(mount_dir)
    for rel, stat in sorted(current.items()):
      if snapshot.get(rel) == stat: continue
      if stat[0] == 'd':
        logger.debug(f"making directory {rel}")
        self.makedirs(rel, exist_ok=True)
      else:
        logger.debug(f"copying back {rel}")
        with (mount_dir / rel).open('rb') as fr:
          with self.open(rel, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
    for rel in sorted(copied - current.keys(), key=lambda rel: -rel.count('/')):
      if snapshot.get(rel, ('',))[0] == 'd':
        logger.debug(f"removing directory {rel}")
        try: self.rm(rel, recursive=True)
        except FileNotFoundError: pass
      else:
        logger.debug(f"removing {rel}")
        try: self.rm_file(rel)
        except FileNotFoundError: pass

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

  def get_drs(self, path, **kwargs):
    with self.__masquerade_os_error(path=path):
      return self.fs.get_drs(self._resolve_path(path), **kwargs)

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

def _snapshot(mount_dir):
  ''' Relative path => ('d',) for directories or ('f', size, mtime_ns) for files
  '''
  snapshot = {}
  for p in Path(mount_dir).rglob('*'):
    rel = str(p.relative_to(mount_dir))
    if p.is_dir():
      snapshot[rel] = ('d',)
    elif p.is_file():
      st = p.stat()
      snapshot[rel] = ('f', st.st_size, st.st_mtime_ns)
  return snapshot

def _wait_for_newer_mtime(snapshot, margin_ns=20_000_000, max_wait_ns=1_000_000_000):
  ''' File mtimes come from a coarse clock, so a modification made right after the snapshot
  could keep the same size & mtime and go unnoticed. Like git's "racy" timestamp handling, we wait
  until the clock is past the newest mtime in the snapshot so that later writes get newer mtimes.
  '''
  import time
  newest = max((stat[2] for stat in snapshot.values() if stat[0] == 'f'), default=None)
  if newest is None: return
  deadline = time.time_ns() + max_wait_ns
  while time.time_ns() <= newest + margin_ns and time.time_ns() < deadline:
    time.sleep(0.005)
