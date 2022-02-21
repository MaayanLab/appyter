import fsspec
import contextlib
import logging

logger = logging.getLogger(__name__)

from appyter.ext.fsspec.chroot import ChrootFileSystem
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.contextlib import with_many

class SingletonFileSystemBase(ChrootFileSystem): pass

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
        super().__init__(fs=fs, **kwargs)

      # we've already setup the context for the filesystem
      def __enter__(self):
        return self
      def __exit__(self, type, value, traceback):
        pass

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
