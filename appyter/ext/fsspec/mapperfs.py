import logging
from functools import partial, partialmethod

from appyter.ext.asyncio.helpers import ensure_async, ensure_sync

logger = logging.getLogger(__name__)

from fsspec.asyn import AsyncFileSystem
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
  __enter__ = ensure_sync(__aenter__)
  
  async def __aexit__(self, type, value, traceback):
    pass
  __exit__ = ensure_sync(__aexit__)

  async def _mkdir(self, path, **kwargs):
    raise PermissionError(path)
  mkdir = ensure_sync(_mkdir)
  
  async def _makedirs(self, path, exist_ok=False):
    raise PermissionError(path)
  makedirs = ensure_sync(_makedirs)

  async def _rmdir(self, path):
    raise PermissionError(path)
  rmdir = ensure_sync(_rmdir)

  async def _rm_file(self, path):
    raise PermissionError(path)
  rm_file = ensure_sync(_rm_file)

  async def _rm(self, path, recursive=False, maxdepth=None):
    raise PermissionError(path)
  rm = ensure_sync(_rm)

  async def _cat_file(self, path, start=None, end=None, **kwargs):
    fs, fs_path = self._pathmap(path)
    return await ensure_async(fs.cat_file)(fs_path, start=start, end=end, **kwargs)
  cat_file = ensure_sync(_cat_file)

  async def _copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    raise PermissionError(path2)
  copy = ensure_sync(_copy)

  async def _mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    raise PermissionError(path1)
  mv = ensure_sync(_mv)

  async def _exists(self, path, **kwargs):
    return path in self.listing or path in self.pathmap
  exists = ensure_sync(_exists)

  async def _info(self, path, **kwargs):
    if path in self.listing:
      return {
        'name': path,
        'type': 'directory',
      }
    else:
      fs, fs_path = self._pathmap(path)
      info = await ensure_async(fs.info)(fs_path, **kwargs)
      info = dict(info, name=path)
      return info
  info = ensure_sync(_info)

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
  ls = ensure_sync(_ls)

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
