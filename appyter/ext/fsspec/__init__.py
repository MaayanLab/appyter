import fsspec

from appyter.ext.fsspec.chroot import ChrootFileSystem
fsspec.register_implementation('chroot', ChrootFileSystem)

from appyter.ext.fsspec.pathmap import PathMapFileSystem
fsspec.register_implementation('pathmap', PathMapFileSystem)
