import contextlib
import logging
import multiprocessing as mp

logger = logging.getLogger(__name__)

def _fuse_run(fs_json, mount_dir, alias_dump, singleton_dump):
  import fsspec.fuse
  import appyter.ext.fsspec
  from appyter.ext.asyncio.event_loop import with_event_loop
  from appyter.ext.fsspec.alias import register_aliases
  from appyter.ext.fsspec.singleton import register_singletons
  from appyter.ext.fsspec.spec import ComposableAbstractFileSystem
  with with_event_loop():
    register_aliases(alias_dump)
    with register_singletons(singleton_dump):
      fs = ComposableAbstractFileSystem.from_json(fs_json)
      logger.debug(f'preparing {fs}..')
      with fs as fs:
        logger.debug('launching fuse..')
        fsspec.fuse.run(fs, '', mount_dir)
        logger.debug('teardown..')

@contextlib.asynccontextmanager
async def fs_mount(fs, mount_dir=None):
  import os
  import signal
  import traceback
  from appyter.ext.fsspec.alias import dump_aliases
  from appyter.ext.fsspec.singleton import dump_singletons
  from appyter.ext.asyncio.try_n_times import async_try_n_times
  from appyter.ext.asyncio.helpers import ensure_async
  from appyter.ext.tempfile import tempdir
  def assert_true(val): assert val
  with tempdir(mount_dir) as mount_dir:
    logger.debug(f'mounting {fs} onto {mount_dir}')
    proc = mp.Process(
      target=_fuse_run,
      args=(fs.to_json(), str(mount_dir), dump_aliases(), dump_singletons()),
    )
    proc.start()
    try:
      await async_try_n_times(3, ensure_async(lambda path: assert_true(path.is_mount())), mount_dir)
      logger.debug(f"fs mount ready on {mount_dir}")
      yield mount_dir
    except Exception as e:
      logger.error(traceback.format_exc())
      raise
    finally:
      if proc.pid:
        logger.debug(f"unmounting fs from {mount_dir}")
        os.kill(proc.pid, signal.SIGINT) # SIGINT cleanly stops fsspec.fuse.run
        logger.debug(f"waiting for process to end")
        await ensure_async(proc.join)()
        await async_try_n_times(3, ensure_async(lambda path: assert_true(not path.is_mount())), mount_dir)
    logger.debug(f"done")
