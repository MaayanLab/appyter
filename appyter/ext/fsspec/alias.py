import logging

logger = logging.getLogger(__name__)

import fsspec
from appyter.ext.fsspec.chroot import ChrootFileSystem
from appyter.ext.fsspec.core import url_to_fs_ex

class AliasFileSystemBase(ChrootFileSystem): pass

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
      fs, fo = url_to_fs_ex(_fs_url, **_kwargs)
      super().__init__(fs=fs, fo=fo, **kwargs)

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
