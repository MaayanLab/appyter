import logging

logger = logging.getLogger(__name__)

import fsspec
import contextlib
from fsspec import AbstractFileSystem
from appyter.ext.fsspec.spec import MountableAbstractFileSystem
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.asyncio.helpers import ensure_sync

class AliasFileSystemBase(MountableAbstractFileSystem, AbstractFileSystem): pass

def AliasFileSystemFactory(_proto, _fs_url, **_kwargs):
  logger.debug(f"creating AliasFileSystem {_proto}://* => {_fs_url}*")
  class AliasFileSystem(AliasFileSystemBase):
    ''' alias: seemless passthrough to a more elaborate protocol
    '''
    root_marker = ''
    protocol = _proto
    fs_url = _fs_url
    kwargs = _kwargs

    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.fs = url_to_chroot_fs(_fs_url, **_kwargs)
      self.root_marker = self.fs.root_marker

    def __enter__(self):
      if getattr(self.fs, '__enter__', None) is not None:
        self.fs.__enter__()
      return self
    
    def __exit__(self, type, value, traceback):
      if getattr(self.fs, '__exit__', None) is None:
        self.fs.__exit__(type, value, traceback)

    async def __aenter__(self):
      if getattr(self.fs, '__aenter__', None) is not None:
        await self.fs.__aenter__()
      return self
    
    async def __aexit__(self, type, value, traceback):
      if getattr(self.fs, '__aexit__', None) is None:
        await self.fs.__aexit__(type, value, traceback)

    @contextlib.asynccontextmanager
    async def _mount(self, mount_dir=None, **kwargs):
      _mount = self.fs._mount if getattr(self.fs, '_mount', None) else MountableAbstractFileSystem._mount
      async with _mount(mount_dir=mount_dir, **kwargs) as mount_dir:
        yield mount_dir
    mount = ensure_sync(_mount)

    def mkdir(self, path, **kwargs):
      return self.fs.mkdir(path, **kwargs)

    def makedirs(self, path, exist_ok=False):
      return self.fs.makedirs(path, exist_ok=exist_ok)

    def rmdir(self, path):
      return self.fs.rmdir(path)

    def rm_file(self, path):
      return self.fs.rm_file(path)

    def rm(self, path, recursive=False, maxdepth=None):
      return self.fs.rm(path, recursive=recursive, maxdepth=maxdepth)

    def cat_file(self, path, start=None, end=None, **kwargs):
      return self.fs.cat_file(path, start=start, end=end, **kwargs)

    def put_file(self, lpath, rpath, **kwargs):
      return self.fs.put_file(lpath, rpath, **kwargs)

    def get_file(self, rpath, lpath, **kwargs):
      return self.fs.get_file(rpath, lpath, **kwargs)

    def cp_file(self, path1, path2, **kwargs):
      return self.fs.cp_file(path1, path2, **kwargs)

    def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
      return self.fs.copy(path1, path2, recursive=recursive, on_error=on_error, **kwargs)

    def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
      return self.fs.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)

    def info(self, path, **kwargs):
      return self.fs.info(path, **kwargs)

    def ls(self, path, detail=True, **kwargs):
      return self.fs.ls(path, detail=detail, **kwargs)

    def _open(self, path, mode="rb", block_size=None, cache_options=None, **kwargs):
      return self.fs._open(path, mode=mode, block_size=block_size, cache_options=cache_options, **kwargs)

  return AliasFileSystem

def dump_aliases():
  return {
    k: [[cls.protocol, cls.fs_url], cls.kwargs]
    for k, cls in fsspec.registry.target.items()
    if issubclass(cls, AliasFileSystemBase)
  }

def register_aliases(alias_dump):
  for k, (args, kwargs) in alias_dump.items():
    fsspec.register_implementation(k, AliasFileSystemFactory(*args, **kwargs))
