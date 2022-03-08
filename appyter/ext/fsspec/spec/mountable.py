import typing as t
import pathlib
import contextlib
from fsspec import AbstractFileSystem

import logging
logger = logging.getLogger(__name__)

class MountableAbstractFileSystem:
  @contextlib.contextmanager
  def mount(self: AbstractFileSystem, path='', mount_dir: t.Optional[pathlib.Path]=None, fuse=False, **kwargs):
    ''' Mount this filesystem
    '''
    logger.debug(f"{self} mount {path} on {mount_dir} ({fuse=})")
    if fuse:
      from appyter.ext.asyncio.helpers import ensure_sync
      from appyter.ext.fsspec.fuse import fs_mount
      with ensure_sync(fs_mount(self, path, mount_dir=mount_dir)) as mount_dir:
        yield mount_dir
    else:
      import shutil
      from appyter.ext.tempfile import tempdir
      # can't use fuse, default is to just copy files into the mount_dir
      with tempdir(mount_dir) as mount_dir:
        logger.debug(f"copying files over...")
        for f1_rel in self.glob('/'.join(filter(None, (path, '**',))), detail=True).values():
          if not f1_rel['name'].startswith(path): raise RuntimeError
          f2_rel = mount_dir / f1_rel['name'][len(path):]
          f2_rel.parent.mkdir(parents=True, exist_ok=True)
          if not f2_rel.exists():
            if f1_rel['type'] == 'file':
              logger.debug(f"copying {f1_rel['name']} to {str(f2_rel)}")
              # TODO: if we're backed by a normal filesystem, make a link
              with self.open(f1_rel['name'], 'rb') as fr:
                with f2_rel.open('wb') as fw:
                  shutil.copyfileobj(fr, fw)
            elif f1_rel['type'] == 'directory':
              logger.debug(f"making directory {f1_rel['name']}")
              f2_rel.mkdir(exist_ok=True)
            else:
              raise NotImplementedError
        logger.debug('Ready')
        yield mount_dir
