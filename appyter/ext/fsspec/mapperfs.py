import logging
logger = logging.getLogger(__name__)

from fsspec import AbstractFileSystem
from fsspec.core import url_to_fs
from appyter.ext.fsspec.util import split_protocol_opts

class MapperFileSystem(AbstractFileSystem):
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

  def _pathmap(self, path):
    ''' Return (fs, path) depending on whether we hit a mapped paths or not
    '''
    if path in self.pathmap:
      from fsspec import filesystem
      protocol, path, opts = split_protocol_opts(self.pathmap[path])
      return url_to_fs(f"{protocol}://{path}", **opts)
    else:
      raise FileNotFoundError(path)

  def __enter__(self):
    return self
  
  def __exit__(self, type, value, traceback):
    pass

  def mkdir(self, path, **kwargs):
    raise PermissionError(path)
  
  def makedirs(self, path, exist_ok=False):
    raise PermissionError(path)

  def rmdir(self, path):
    raise PermissionError(path)

  def rm(self, path, recursive=False, maxdepth=None):
    raise PermissionError(path)

  def copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    raise PermissionError(path2)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    raise PermissionError(path1)

  def exists(self, path, **kwargs):
    return path in self.listing or path in self.pathmap

  def info(self, path, **kwargs):
    if path in self.listing:
      return {
        'name': path,
        'type': 'directory',
      }
    else:
      fs, fs_path = self._pathmap(path)
      info = fs.info(fs_path, **kwargs)
      info = dict(info, name=path)
      return info

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
    return results

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    fs, fs_path = self._pathmap(path)
    if 'r' not in mode: raise PermissionError(path)
    return fs._open(
      fs_path,
      mode=mode,
      block_size=block_size,
      autocommit=autocommit,
      cache_options=cache_options,
      **kwargs,
    )
