import contextlib
import logging
from multiprocessing import Process

logger = logging.getLogger(__name__)

def _fuse_run(url, mount_point, kwargs, alias_dump, singleton_dump):
  import fsspec.fuse
  from appyter.ext.fsspec.core import url_to_chroot_fs
  from appyter.ext.fsspec.alias import register_aliases
  from appyter.ext.fsspec.singleton import register_singletons
  register_aliases(alias_dump)
  logger.debug(f'preparing fs from {url} ({kwargs})..')
  with register_singletons(singleton_dump):
    with url_to_chroot_fs(url, **kwargs) as fs:
      logger.debug('launching fuse..')
      fsspec.fuse.run(fs, '', mount_point)
      logger.debug('teardown..')

@contextlib.asynccontextmanager
async def fs_mount(url, **kwargs):
  import os
  import signal
  import asyncio
  import pathlib
  import traceback
  from appyter.ext.fsspec.alias import dump_aliases
  from appyter.ext.fsspec.singleton import dump_singletons
  from appyter.ext.asyncio.try_n_times import async_try_n_times
  from appyter.ext.asyncio.run_in_executor import run_in_executor
  from appyter.ext.pathlib.assertions import async_assert_mounted, async_assert_unmounted
  @run_in_executor
  def _rmdir(path):
    path.rmdir()
  tmp = pathlib.Path(tempfile.mkdtemp())
  logger.debug(f'mounting {url} onto {tmp}')
  proc = Process(
    target=_fuse_run, args=(url, str(tmp), kwargs, dump_aliases(), dump_singletons())
  )
  proc.start()
  try:
    await async_try_n_times(3, async_assert_mounted, tmp)
    logger.debug(f"fs mount ready on {tmp}")
    yield tmp
  except Exception as e:
    logger.error(traceback.format_exc())
    raise
  finally:
    if proc.pid:
      logger.debug(f"unmounting fs from {tmp}")
      os.kill(proc.pid, signal.SIGINT) # SIGINT cleanly stops fsspec.fuse.run
      logger.debug(f"waiting for process to end")
      await asyncio.get_running_loop().run_in_executor(None, proc.join)
      await async_try_n_times(3, async_assert_unmounted, tmp)
      await async_try_n_times(3, _rmdir, tmp)
  logger.debug(f"done")
