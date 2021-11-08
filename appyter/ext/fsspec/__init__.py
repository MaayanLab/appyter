import fsspec

from appyter.ext.fsspec.writecache import WriteCacheFileSystem
fsspec.register_implementation('writecache', WriteCacheFileSystem)

from appyter.ext.fsspec.chroot import ChrootFileSystem
fsspec.register_implementation('chroot', ChrootFileSystem)

from appyter.ext.fsspec.alias import AliasFileSystemFactory
fsspec.register_implementation('tmpfs', AliasFileSystemFactory('tmpfs', 'memory://'))
