import fsspec
import contextlib
import traceback
import logging
from appyter.ext.asyncio.try_n_times import try_n_times
logger = logging.getLogger(__name__)

from appyter.ext.fsspec.chroot import ChrootFileSystem, url_to_chroot_fs
fsspec.register_implementation('chroot', ChrootFileSystem)

from appyter.ext.fsspec.pathmap import PathMapFileSystem
fsspec.register_implementation('pathmap', PathMapFileSystem)

from appyter.ext.fsspec.alias import AliasFileSystemFactory
fsspec.register_implementation('tmpfs', AliasFileSystemFactory('tmpfs', 'memory://'))

@contextlib.asynccontextmanager
async def fs_mount(fs, path):
  import os
  import signal
  import asyncio
  import pathlib
  import tempfile
  import fsspec.fuse
  from multiprocessing import Process
  from appyter.ext.asyncio.run_in_executor import run_in_executor
  logging.getLogger('fsspec.fuse').setLevel(logging.WARNING)
  @run_in_executor
  def assert_mounted(path):
    assert path.is_mount()
  @run_in_executor
  def assert_not_mounted(path):
    assert not path.is_mount()
  @run_in_executor
  def rmdir(path):
    path.rmdir()
  tmp = pathlib.Path(tempfile.mkdtemp())
  logger.debug(f'mounting fs onto {tmp}')
  loop = asyncio.get_running_loop()
  proc = Process(target=fsspec.fuse.run, args=(fs, path, str(tmp)))
  proc.start()
  try:
    await try_n_times(3, assert_mounted, tmp)
    logger.debug(f"fs mount ready on {tmp}")
    yield tmp
  except:
    logger.error(traceback.format_exc())
    raise
  finally:
    logger.debug(f"unmounting fs from {tmp}")
    os.kill(proc.pid, signal.SIGINT) # SIGINT cleanly stops fsspec.fuse.run
    logger.debug(f"waiting for process to end")
    await loop.run_in_executor(None, proc.join)
    await try_n_times(3, assert_not_mounted, tmp)
    await try_n_times(3, rmdir, tmp)
  logger.debug(f"done")
