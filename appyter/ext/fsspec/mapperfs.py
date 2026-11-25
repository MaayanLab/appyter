import logging
from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem

from appyter.ext.urllib import join_slash
logger = logging.getLogger(__name__)

from fsspec import AbstractFileSystem
from appyter.ext.fsspec.spec.mountable import MountableAbstractFileSystem
from appyter.ext.fsspec.core import url_to_fs_ex

class MapperFileSystem(MountableAbstractFileSystem, AbstractFileSystem):
  ''' MapperFS is the inverse of a fsspec.mapper -- it lets you use a mapping to
  define a virtual filesystem.
  '''
  root_marker = ''
  protocol = 'mapperfs'

  def __init__(self, pathmap={}, **kwargs):
    '''
    Parameters
    ----------
    pathmap: dict
      A mapping from [path to map onto the target filesystem]: filesystem url to present
    '''
    super().__init__(**kwargs)
    if not pathmap:
      raise ValueError(
          "pathmap is required"
      )
    
    self.pathmap = {}
    for path, fs_uri in pathmap.items():
      if type(fs_uri) == str:
        self.pathmap[path] = url_to_fs_ex(fs_uri)
      elif type(fs_uri) == tuple or type(fs_uri) == list:
        self.pathmap[path] = fs_uri
      else:
        self.pathmap[path] = fs_uri, ''

    # mapped files we had to download locally (see info)
    self._materialized = {}

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

  def _pathmap(self, path):
    ''' Return (fs, path) depending on whether we hit a mapped paths or not
    '''
    if path in self.pathmap:
      return (*self.pathmap[path], path)
    else:
      path_split = path.split('/')
      for i in range(1, len(path_split)):
        base_path = '/'.join(path_split[:-i])
        if base_path in self.pathmap:
          fs, fo = self.pathmap[base_path]
          return fs, join_slash(fo, *path_split[-i:]), base_path
      raise FileNotFoundError(path)

  def __enter__(self):
    for fs, _fo in self.pathmap.values():
      if getattr(fs, '__enter__', None) is not None:
        fs.__enter__()
    return self

  def __exit__(self, type, value, traceback):
    for fs, _fo in self.pathmap.values():
      if getattr(fs, '__exit__', None) is not None:
        fs.__exit__(type, value, traceback)

  def mkdir(self, path, **kwargs):
    raise PermissionError(path)
  
  def makedirs(self, path, exist_ok=False):
    raise PermissionError(path)

  def rmdir(self, path):
    raise PermissionError(path)

  def rm_file(self, path):
    raise PermissionError(path)

  def rm(self, path, recursive=False, maxdepth=None):
    raise PermissionError(path)

  def cat_file(self, path, start=None, end=None, **kwargs):
    fs, fs_path, _ = self._pathmap(path)
    return fs.cat_file(fs_path, start=start, end=end, **kwargs)

  def copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    raise PermissionError(path2)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    raise PermissionError(path1)

  def exists(self, path, **kwargs):
    return path in self.listing or path in self.pathmap

  def get_drs(self, path, **kwargs):
    if path in self.listing:
      raise IsADirectoryError
    else:
      fs, fs_path, _ = self._pathmap(path)
      return fs.get_drs(fs_path, **kwargs)

  def info(self, path, **kwargs):
    if path in self.listing:
      return {
        'name': path,
        'type': 'directory',
      }
    elif path in self._materialized:
      import os
      return {'name': path, 'type': 'file', 'size': os.path.getsize(self._materialized[path])}
    else:
      fs, fs_path, _ = self._pathmap(path)
      info = fs.info(fs_path, **kwargs)
      info = dict(info, name=path)
      if info.get('type') == 'file' and info.get('size') is None:
        # the size is unknown (e.g. a streamed http response without a Content-Length),
        #  which fuse requires, so we fetch the file once and serve it locally from then on
        import os
        info['size'] = os.path.getsize(self._materialize(path))
      return info

  def _is_http(self, path):
    fs, _fs_path, _ = self._pathmap(path)
    protocols = fs.protocol if isinstance(fs.protocol, (tuple, list)) else (fs.protocol,)
    return any(p in {'http', 'https'} for p in protocols)

  def _materialize(self, path):
    ''' Download a mapped file to a local temporary file, returning its path
    '''
    if path not in self._materialized:
      from appyter.ext.tempfile import mktemp
      fs, fs_path, _ = self._pathmap(path)
      local_path = mktemp()
      logger.debug(f"materializing {path} to {local_path}")
      fs.get_file(fs_path, local_path)
      self._materialized[path] = local_path
    return self._materialized[path]

  def ls(self, path, detail=False, **kwargs):
    ''' Aggregate results based on pathmap listing & underlying fs
    '''
    logger.debug(f"ls({path})")
    results = []
    if path in self.listing:
      for p in self.listing[path]:
        if detail:
          results.append(self.info(p))
        else:
          results.append(p)
    else:
      try:
        fs, fo, base_path = self._pathmap(path)
        for p in fs.ls(fo, detail=detail):
          if detail:
            results.append(dict(p, name=join_slash(base_path, p['name'])))
          else:
            results.append(join_slash(base_path, p))
      except FileNotFoundError:
        pass
    return results

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    if 'r' not in mode or '+' in mode: raise PermissionError(path)
    if path not in self._materialized and self._is_http(path):
      # http servers may not support the range requests random access relies on,
      #  which we only discover mid-read, so we fetch the file once and serve it locally
      self._materialize(path)
    if path in self._materialized:
      from fsspec.implementations.local import LocalFileOpener
      return LocalFileOpener(self._materialized[path], mode)
    fs, fs_path, _ = self._pathmap(path)
    return fs._open(
      fs_path,
      mode=mode,
      block_size=block_size,
      autocommit=autocommit,
      cache_options=cache_options,
      **kwargs,
    )

  def to_json(self):
    import json
    cls = type(self)
    cls = '.'.join((cls.__module__, cls.__name__))
    proto = (
      self.protocol[0]
      if isinstance(self.protocol, (tuple, list))
      else self.protocol
    )
    return json.dumps(
      dict(
        **{"cls": cls, "protocol": proto, "args": self.storage_args},
        **dict(
          self.storage_options,
          pathmap={
            path: [json.loads(fs.to_json()), fo]
            for path, (fs, fo) in self.pathmap.items()
          },
        )
      )
    )

  @staticmethod
  def from_json(blob):
    import json
    from fsspec.registry import _import_class, get_filesystem_class
    dic = json.loads(blob)
    protocol = dic.pop("protocol")
    try:
      cls = _import_class(dic.pop("cls"))
    except (ImportError, ValueError, RuntimeError, KeyError, AttributeError):
      cls = get_filesystem_class(protocol)
    if cls.from_json == MapperFileSystem.from_json:
      return cls(
        *dic.pop("args", ()),
        pathmap={
          path: (ComposableAbstractFileSystem.from_json(json.dumps(fs)), fo)
          for path, [fs, fo] in dic.pop('pathmap').items()
        },
        **dic,
      )
    else:
      return cls.from_json(blob)
