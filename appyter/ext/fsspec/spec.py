import typing as t
import pathlib
import contextlib
from fsspec import AbstractFileSystem

import logging
logger = logging.getLogger(__name__)

class MountableAbstractFileSystem:
  @contextlib.contextmanager
  def mount(self: AbstractFileSystem, mount_dir: t.Optional[pathlib.Path]=None, fuse=False, **kwargs):
    ''' Mount this filesystem
    '''
    logger.info(f"{self=} mount {mount_dir=} {fuse=}")
    if fuse:
      from appyter.ext.asyncio.helpers import ensure_sync
      from appyter.ext.fsspec.fuse import fs_mount
      with ensure_sync(fs_mount(self, mount_dir=mount_dir)) as mount_dir:
        yield mount_dir
    else:
      import shutil
      from appyter.ext.tempfile import tempdir
      # can't use fuse, default is to just copy files into the mount_dir
      with tempdir(mount_dir) as mount_dir:
        logger.info(f"copying files over...")
        for f1_rel in self.glob('**/*'):
          logger.info(f"copying {f1_rel}")
          f2_rel = mount_dir / f1_rel
          f2_rel.parent.mkdir(parents=True, exist_ok=True)
          if not f2_rel.exists():
            # TODO: if we're backed by a normal filesystem, make a link
            with self.open(f1_rel, 'rb') as fr:
              with f2_rel.open('wb') as fw:
                shutil.copyfileobj(fr, fw)
        logger.info('Ready')
        yield mount_dir

class ComposableAbstractFileSystem:
  ''' Expansion of AbstractFileSystem's json serialization methods to support composition
  by calling to_json() on any filesystems in storage_args during serialization,
  and loading them in during deserialization.
  '''
  def to_json(self):
    import json
    cls = type(self)
    cls = '.'.join((cls.__module__, cls.__name__))
    proto = (
      self.protocol[0]
      if isinstance(self.protocol, (tuple, list))
      else self.protocol
    )
    return json.dumps(
      dict(
        **{"cls": cls, "protocol": proto, "args": self.storage_args},
        **{
          k: json.loads(v.to_json()) if isinstance(v, AbstractFileSystem) else v
          for k, v in self.storage_options.items()
        },
      )
    )

  @staticmethod
  def from_json(blob):
    import json
    from fsspec.registry import _import_class, get_filesystem_class
    dic = json.loads(blob)
    protocol = dic.pop("protocol")
    try:
      cls = _import_class(dic.pop("cls"))
    except (ImportError, ValueError, RuntimeError, KeyError):
      cls = get_filesystem_class(protocol)
    return cls(*dic.pop("args", ()), **{
      k: ComposableAbstractFileSystem.from_json(json.dumps(v)) if type(v) == dict and 'cls' in v else v
      for k, v in dic.items()
    })
