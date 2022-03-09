import typing as t
import pathlib
import contextlib
from fsspec import AbstractFileSystem

import logging
logger = logging.getLogger(__name__)

class MountableAbstractFileSystem:
  @contextlib.contextmanager
  def mount(self: AbstractFileSystem, path='', passthrough=False, **kwargs):
    ''' mount fallback: defer to chroot-filesystem
    '''
    from appyter.ext.fsspec.chroot import ChrootFileSystem
    fs = self if isinstance(self, ChrootFileSystem) else ChrootFileSystem(fs=self, fo=path)
    with fs.mount(path=path, passthrough=False, **kwargs) as mount_dir:
      yield mount_dir
