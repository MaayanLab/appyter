import contextlib
import logging
import multiprocessing as mp

logger = logging.getLogger(__name__)

import time, stat, fuse, errno, traceback
from fsspec.fuse import FUSEr
class FUSErEx(FUSEr):
  def getattr(self, path, fh=None):
      if self._ready_file and path in ["/.fuse_ready", ".fuse_ready"]:
          return {"type": "file", "st_size": 5}

      path = "".join([self.root, path.lstrip("/")]).rstrip("/")
      try:
          if len(path) > 255:
             raise fuse.FuseOSError(errno.ENAMETOOLONG)
          info = self.fs.info(path)
      except:
          logger.warning(traceback.format_exc())
          raise fuse.FuseOSError(errno.ENOENT)

      data = {"st_uid": info.get("uid", 1000), "st_gid": info.get("gid", 1000)}
      perm = info.get("mode", 0o777)

      if info["type"] != "file":
          data["st_mode"] = stat.S_IFDIR | perm
          data["st_size"] = 0
          data["st_blksize"] = 0
      else:
          data["st_mode"] = stat.S_IFREG | perm
          data["st_size"] = info["size"]
          data["st_blksize"] = 5 * 2 ** 20
          data["st_nlink"] = 1
      data["st_atime"] = time.time()
      data["st_ctime"] = time.time()
      data["st_mtime"] = time.time()
      return data

def _fuse_run(fs_json, fs_path, mount_dir):
  import fsspec.fuse
  import appyter.ext.fsspec
  from appyter.ext.asyncio.event_loop import with_event_loop
  from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem
  with with_event_loop():
    fs = ComposableAbstractFileSystem.from_json(fs_json)
    logger.debug(f'preparing {fs}..')
    with fs as fs:
      logger.debug('launching fuse..')
      fsspec.fuse.run(fs, fs_path, mount_dir, threads=True, ops_class=FUSErEx)
      logger.debug('teardown..')

@contextlib.asynccontextmanager
async def fs_mount(fs, fs_path='', mount_dir=None):
  import os
  import signal
  import traceback
  from appyter.ext.asyncio.try_n_times import async_try_n_times
  from appyter.ext.asyncio.helpers import ensure_async
  from appyter.ext.tempfile import tempdir
  def assert_true(val): assert val
  with tempdir(mount_dir) as mount_dir:
    logger.debug(f'mounting {fs} onto {mount_dir}')
    proc = mp.Process(
      target=_fuse_run,
      args=(fs.to_json(), str(fs_path), str(mount_dir)),
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
        try:
          await ensure_async(proc.join)(30)
        except TimeoutError:
          os.kill(proc.pid, signal.SIGTERM) # SIGTERM unclean stop
        await async_try_n_times(3, ensure_async(lambda path: assert_true(not path.is_mount())), mount_dir)
    logger.debug(f"done")
