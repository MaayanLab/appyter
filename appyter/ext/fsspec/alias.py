import logging
logger = logging.getLogger(__name__)

from fsspec import AbstractFileSystem
from appyter.ext.fsspec.core import url_to_chroot_fs

def AliasFileSystemFactory(proto, fs_url, **_kwargs):
  logger.debug(f"creating AliasFileSystem {proto}:/// => {fs_url}")
  class AliasFileSystem(AbstractFileSystem):
    ''' alias: seemless passthrough to a more elaborate protocol
    '''
    root_marker = '/'
    protocol = proto

    def __init__(self, **kwargs):
      super().__init__(**kwargs)
      self.fs = url_to_chroot_fs(fs_url, **_kwargs)

    def __enter__(self):
      if getattr(self.fs, '__enter__', None) is not None:
        self.fs.__enter__()
      return self
    
    def __exit__(self, type, value, traceback):
      if getattr(self.fs, '__exit__', None) is None:
        self.fs.__exit__(type, value, traceback)

    def mkdir(self, path, **kwargs):
      return self.fs.mkdir(path, **kwargs)

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

  return AliasFileSystem
