import logging
logger = logging.getLogger(__name__)

from fsspec.asyn import AsyncFileSystem, sync_wrapper
from appyter.ext.fsspec.spec import MountableAbstractFileSystem
from appyter.ext.fsspec.core import url_to_fs_ex

class MapperFileSystem(MountableAbstractFileSystem, AsyncFileSystem):
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
      return url_to_fs_ex(self.pathmap[path])
    else:
      raise FileNotFoundError(path)

  async def __aenter__(self):
    return self
  __enter__ = sync_wrapper(__aenter__)
  
  async def __aexit__(self, type, value, traceback):
    pass
  __exit__ = sync_wrapper(__aexit__)

  async def _mkdir(self, path, **kwargs):
    raise PermissionError(path)
  mkdir = sync_wrapper(_mkdir)
  
  async def _makedirs(self, path, exist_ok=False):
    raise PermissionError(path)
  makedirs = sync_wrapper(_makedirs)

  async def _rmdir(self, path):
    raise PermissionError(path)
  rmdir = sync_wrapper(_rmdir)

  async def _rm_file(self, path):
    raise PermissionError(path)
  rm_file = sync_wrapper(_rm_file)

  async def _rm(self, path, recursive=False, maxdepth=None):
    raise PermissionError(path)
  rm = sync_wrapper(_rm)

  async def _copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    raise PermissionError(path2)
  copy = sync_wrapper(_copy)

  async def _mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    raise PermissionError(path1)
  mv = sync_wrapper(_mv)

  async def _exists(self, path, **kwargs):
    return path in self.listing or path in self.pathmap
  exists = sync_wrapper(_exists)

  async def _info(self, path, **kwargs):
    if path in self.listing:
      return {
        'name': path,
        'type': 'directory',
      }
    else:
      fs, fs_path = self._pathmap(path)
      if getattr(fs, '_info', None) is not None:
        info = await fs._info(fs_path, **kwargs)
      else:
        info = fs.info(fs_path, **kwargs)
      info = dict(info, name=path)
      return info
  info = sync_wrapper(_info)

  async def _ls(self, path, detail=False, **kwargs):
    ''' Aggregate results based on pathmap listing & underlying fs
    '''
    logger.debug(f"ls({path})")
    results = []
    if path in self.listing:
      for p in self.listing[path]:
        if detail:
          results.append(await self._info(p))
        else:
          results.append(p)
    return results
  ls = sync_wrapper(_ls)

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
