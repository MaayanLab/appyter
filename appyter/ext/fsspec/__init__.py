import fsspec

from appyter.ext.fsspec.chroot import ChrootFileSystem
fsspec.register_implementation('chroot', ChrootFileSystem)

from appyter.ext.fsspec.pathmap import PathMapFileSystem
fsspec.register_implementation('pathmap', PathMapFileSystem)

from appyter.ext.fsspec.alias import AliasFileSystemFactory
fsspec.register_implementation('tmpfs', AliasFileSystemFactory('tmpfs', 'memory://'))
