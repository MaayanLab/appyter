import fsspec

from appyter.ext.fsspec.writecache import WriteCacheFileSystem
fsspec.register_implementation('writecache', WriteCacheFileSystem)

from appyter.ext.fsspec.chroot import ChrootFileSystem
fsspec.register_implementation('chroot', ChrootFileSystem)

from appyter.ext.fsspec.sbfs import SBFSFileSystem
fsspec.register_implementation('sbfs', SBFSFileSystem)

from appyter.ext.fsspec.drs import DRSFileSystem
fsspec.register_implementation('drs', DRSFileSystem)
