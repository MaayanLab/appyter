import fsspec

from appyter.ext.fsspec.writecache import WriteCacheFileSystem
fsspec.register_implementation('writecache', WriteCacheFileSystem)

from appyter.ext.fsspec.chroot import ChrootFileSystem
fsspec.register_implementation('chroot', ChrootFileSystem)

from appyter.ext.fsspec.sbfs import SBFSFileSystem
fsspec.register_implementation('sbfs', SBFSFileSystem)

from appyter.ext.fsspec.drs import DRSFileSystem
fsspec.register_implementation('drs', DRSFileSystem)

from appyter.ext.fsspec.s3fs import S3FileSystemEx
fsspec.register_implementation('s3', S3FileSystemEx)
