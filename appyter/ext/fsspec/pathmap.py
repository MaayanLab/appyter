import shutil
from fsspec import filesystem, AbstractFileSystem
from fsspec.core import url_to_fs
from appyter.ext.fsspec.parse import parse_file_uri_qs
from appyter.ext.urllib import join_slash

class PathMapFileSystem(AbstractFileSystem):
  ''' Pathmap layer over any other FS. Typically one would use a chroot as a base
  filesystem, so instantiation would look like:
  `pathmap::chroot::proto://underyling-fs`
  '''
  root_marker = ''
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
      for i in range(len(src_split)):
        p = '/'.join(src_split[:i+1])
        if i == 0:
          if '' not in self.listing:
            self.listing[''] = {}
          if p:
            self.listing[''][p] = True
        else:
          self.listing['/'.join(src_split[:i])][p] = True
        if i < len(src_split)-1:
          if p not in self.listing:
            self.listing[p] = {}

  def __pathmap(self, path):
    ''' Return (fs, path, mode) depending on whether we hit a mapped paths or not
    '''
    if path in self.pathmap:
      url, qs = parse_file_uri_qs(self.pathmap[path])
      fs, path = url_to_fs(url, **qs)
      mode = 0o444
    else:
      fs, path = self.fs, join_slash(self.storage_options['fo'], path)
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
    fs, path, mode = self.__pathmap(path)
    if mode == 0o444: raise PermissionError
    return fs.mkdir(path, **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    fs, path, mode = self.__pathmap(path)
    if mode == 0o444: raise PermissionError
    return fs.rm(path, recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    fs1, path1, mode1 = self.__pathmap(path1)
    fs2, path2, mode2 = self.__pathmap(path2)
    if mode2 == 0o444: raise PermissionError
    if fs1 == fs2:
      return fs1.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)
    else:
      if fs1.isdir(path1) and recursive:
        for f1 in fs1.walk(path1, maxdepth=maxdepth):
          f_rel = f1.replace(path1, '')
          f2_rel = join_slash(path2, f_rel)
          with fs1.open(f1, 'rb') as fr:
            with fs2.open(f2_rel, 'wb') as fw:
              shutil.copyfileobj(fr, fw)
      else:
        with fs1.open(path1, 'rb') as fr:
          with fs2.open(path2, 'wb') as fw:
            shutil.copyfileobj(fr, fw)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    fs1, path1, mode1 = self.__pathmap(path1)
    fs2, path2, mode2 = self.__pathmap(path2)
    if mode1 == 0o444: raise PermissionError
    if mode2 == 0o444: raise PermissionError
    if fs1 == fs2:
      return fs1.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)
    else:
      if fs1.isdir(path1) and recursive:
        for f1 in fs1.walk(path1, maxdepth=maxdepth):
          f_rel = f1.replace(path1, '')
          f2_rel = join_slash(path2, f_rel)
          with fs1.open(f1, 'rb') as fr:
            with fs2.open(f2_rel, 'wb') as fw:
              shutil.copyfileobj(fr, fw)
          fs1.rm(f1)
      else:
        with fs1.open(path1, 'rb') as fr:
          with fs2.open(path2, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
        fs1.rm(path1)

  def exists(self, path, **kwargs):
    if path in self.listing:
      return True
    else:
      fs, fs_path, mode = self.__pathmap(path)
      return fs.exists(fs_path, **kwargs)

  def info(self, path, **kwargs):
    if path in self.listing:
      return {
        'name': path,
        'type': 'directory',
        'mode': 0o444,
      }
    else:
      fs, fs_path, mode = self.__pathmap(path)
      info = fs.info(fs_path, **kwargs)
      info = dict(info, name=path, mode=mode)
      return info

  def ls(self, path, detail=False, **kwargs):
    ''' Aggregate results based on pathmap listing & underlying fs
    '''
    results = {}
    if path in self.listing:
      for p in self.listing[path]:
        if detail:
          results[path + p] = self.info(path + p)
        else:
          results[path + p] = path + p
    #
    fs, fs_path, mode = self.__pathmap(path)
    if fs is self.fs:
      for f in fs.ls(fs_path, detail=detail, **kwargs):
        if detail:
          results[f['name']] = f
        else:
          results[f] = f
    #
    return list(results.values())

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    fs, path, fs_mode = self.__pathmap(path)
    if fs_mode == 0o444 and ('w' in mode or '+' in mode): raise PermissionError
    return fs._open(
      path,
      mode=mode,
      block_size=block_size,
      autocommit=autocommit,
      cache_options=cache_options,
      **kwargs,
    )
