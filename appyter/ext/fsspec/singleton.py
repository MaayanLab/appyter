import sys
import fsspec
import contextlib
import logging
logger = logging.getLogger(__name__)

from appyter.ext.fsspec.spec import AbstractFileSystemEx
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.contextlib import with_many

class SingletonFileSystemBase(AbstractFileSystemEx): pass

@contextlib.contextmanager
def SingletonFileSystemFactory(_proto, _fs_url, **_kwargs):
  logger.debug(f"creating SingletonFileSystem {_proto}://* => {_fs_url}*")
  with url_to_chroot_fs(_fs_url, **_kwargs) as fs:
    class SingletonFileSystem(SingletonFileSystemBase):
      ''' passthrough to a filesystem instance
      '''
      root_marker = ''
      protocol = _proto
      fs_url = _fs_url
      kwargs = _kwargs

      def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fs = fs
        self.root_marker = self.fs.root_marker

      def __enter__(self):
        return self
      
      def __exit__(self, type, value, traceback):
        pass

      @contextlib.asynccontextmanager
      async def mount(self, mount_dir, **kwargs):
        _mount = self.fs.mount if getattr(self.fs, 'mount', None) else super().mount
        async with _mount(mount_dir, **kwargs) as mount_dir:
          yield mount_dir

      def mkdir(self, path, **kwargs):
        return self.fs.mkdir(path, **kwargs)

      def makedirs(self, path, exist_ok=False):
        return self.fs.makedirs(path, exist_ok=exist_ok)

      def rmdir(self, path):
        return self.fs.rmdir(path)

      def rm(self, path, recursive=False, maxdepth=None):
        return self.fs.rm(path, recursive=recursive, maxdepth=maxdepth)

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

    yield SingletonFileSystem

def dump_singletons():
  return {
    k: [[cls.protocol, cls.fs_url], cls.kwargs]
    for k, cls in fsspec.registry.target.items()
    if issubclass(cls, SingletonFileSystemBase)
  }

@contextlib.contextmanager
def register_singletons(singleton_dump):
  with with_many(**{
    k: SingletonFileSystemFactory(*args, **kwargs)
    for k, (args, kwargs) in singleton_dump.items()
  }) as singletons:
    for k, singleton in singletons.items():
      fsspec.register_implementation(k, singleton)
    yield
