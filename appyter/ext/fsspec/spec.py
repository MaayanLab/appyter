import shutil
import pathlib
import contextlib
from fsspec import AbstractFileSystem
class AbstractFileSystemEx(AbstractFileSystem):
  @contextlib.asynccontextmanager
  async def mount(self, mount_dir: pathlib.Path, fuse=False, **kwargs):
    ''' Mount this filesystem
    '''
    if fuse:
      from appyter.ext.fsspec.fuse import fs_mount
      async with fs_mount(
        f"{self.protocol}:://",
        mount_dir=mount_dir,
        **{ self.protocol: self.storage_options }
      ) as mount_dir:
        yield mount_dir
    else:
      # can't use fuse, default is to just copy files into the mount_dir
      for f1 in self.walk(''):
        f_rel = f1.replace('', '')
        f2_rel = mount_dir / f_rel
        f2_rel.parent.makedirs(parents=True, exists_ok=True)
        if not f2_rel.exists():
          # TODO: if we're backed by a normal filesystem, make a link
          with self.open(f1, 'rb') as fr:
            with f2_rel.open('wb') as fw:
              shutil.copyfileobj(fr, fw)
      yield mount_dir
