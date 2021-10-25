import shutil
import time
from fsspec import filesystem, AbstractFileSystem
from fsspec.core import url_to_fs

from appyter.ext.urllib import parse_qs

class PathMapFileSystem(AbstractFileSystem):
  ''' Pathmap layer over any other FS. Typically one would use a chroot as a base
  filesystem, so instantiation would look like:
  `pathmap::chroot::file://underyling-fs`
  '''
  root_marker = '/'
  protocol = 'pathmap'

  def __init__(self, target_protocol=None, target_options=None, fs=None, pathmap={}, **kwargs):
    '''
    Parameters
    ----------
    target_protocol: str (optional)
      Target filesystem protocol. Provide either this or ``fs``.
    target_options: dict or None
      Passed to the instantiation of the FS, if fs is None.
    fs: filesystem instance
      The target filesystem to run against. Provide this or ``protocol``.
    pathmap: dict
      A mapping from [path to map onto the target filesystem]: filesystem url to present
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
    self.pathmap = pathmap
    self.listing = {}
    for mapping in self.pathmap:
      src_split = mapping.split('/')
      for i in range(2, len(src_split)):
        path_parent = '/'.join(src_split[:i-1]) + '/'
        path_current = '/'.join(src_split[:i]) + '/'
        if path_parent not in self.listing: self.listing[path_parent] = {}
        self.listing[path_parent][path_current] = True
      path_parent = '/'.join(src_split[:-1]) + '/'
      if path_parent not in self.listing: self.listing[path_parent] = {}
      self.listing[path_parent][src_split[-1]] = True

  def _pathmap(self, path):
    ''' Return (fs, path, mode) depending on whether we hit a mapped paths or not
    '''
    if path in self.pathmap:
      if '?' in self.pathmap[path]:
        url, qs = self.pathmap[path].split('?', maxsplit=1)
        qs = parse_qs(qs)
      else:
        url = self.pathmap[path]
        qs = {}
      fs, path = url_to_fs(url, **qs)
      mode = 0o444
    else:
      fs, path = self.fs, self.storage_options['fo'].rstrip('/') + '/' + path.lstrip('/')
      mode = 0o755
    return fs, path, mode

  def __enter__(self):
    if getattr(self.fs, '__enter__', None) is not None:
      self.fs.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.fs, '__exit__', None) is not None:
      self.fs.__exit__(type, value, traceback)

  def mkdir(self, path, **kwargs):
    fs, path, mode = self._pathmap(path)
    if mode == 0o444: raise PermissionError
    return fs.mkdir(path, **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    fs, path, mode = self._pathmap(path)
    if mode == 0o444: raise PermissionError
    return fs.rm(path, recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    fs1, path1, mode1 = self._pathmap(path1)
    fs2, path2, mode2 = self._pathmap(path2)
    if mode2 == 0o444: raise PermissionError
    if fs1 == fs2:
      return fs1.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)
    else:
      if fs1.isdir(path1) and recursive:
        for f1 in fs1.walk(path1, maxdepth=maxdepth):
          f_rel = f1.replace(path1, '')
          f2_rel = path2.rstrip('/') + '/' + f_rel
          with fs1.open(f1, 'rb') as fr:
            with fs2.open(f2_rel, 'wb') as fw:
              shutil.copyfileobj(fr, fw)
      else:
        with fs1.open(path1, 'rb') as fr:
          with fs2.open(path2, 'wb') as fw:
            shutil.copyfileobj(fr, fw)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    fs1, path1, mode1 = self._pathmap(path1)
    fs2, path2, mode2 = self._pathmap(path2)
    if mode1 == 0o444: raise PermissionError
    if mode2 == 0o444: raise PermissionError
    if fs1 == fs2:
      return fs1.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)
    else:
      if fs1.isdir(path1) and recursive:
        for f1 in fs1.walk(path1, maxdepth=maxdepth):
          f_rel = f1.replace(path1, '')
          f2_rel = path2.rstrip('/') + '/' + f_rel
          with fs1.open(f1, 'rb') as fr:
            with fs2.open(f2_rel, 'wb') as fw:
              shutil.copyfileobj(fr, fw)
          fs1.rm(f1)
      else:
        with fs1.open(path1, 'rb') as fr:
          with fs2.open(path2, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
        fs1.rm(path1)

  def info(self, path, **kwargs):
    if path in self.listing:
      return {
        'name': path,
        'size': 0,
        'type': 'directory',
        'created': time.time(),
        'mtime': time.time(),
        'mode': 0o444,
        'islink': False,
        'uid': 1000,
        'gid': 1000,
      }
    else:
      fs, fs_path, mode = self._pathmap(path)
      info = fs.info(fs_path)
      info['name'] = path
      info['mode'] = mode
      return info

  def ls(self, path, detail=False, **kwargs):
    ''' Aggregate results based on pathmap listing & underlying fs
    '''
    results = {}
    if path in self.listing:
      for p in self.listing[path]:
        if detail:
          results[p] = self.info(path + p.lstrip('/'))
        else:
          results[p] = p
    #
    fs, fs_path, mode = self._pathmap(path)
    for f in fs.ls(fs_path, detail=detail, **kwargs):
      if detail:
        results[f['name']] = f
      else:
        results[f] = f
    #
    return list(results.values())

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    fs, path, fs_mode = self._pathmap(path)
    if fs_mode == 0o444 and 'w' in mode or '+' in mode: raise PermissionError
    return fs._open(
      path,
      mode=mode,
      block_size=block_size,
      autocommit=autocommit,
      cache_options=cache_options,
      **kwargs,
    )
