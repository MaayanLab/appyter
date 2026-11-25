import contextlib
import logging
import multiprocessing as mp

logger = logging.getLogger(__name__)

def _fuser_class():
  ''' fsspec's FUSEr treats any open without O_WRONLY as a read-only open, so
  files opened for reading and writing (e.g. python's `open(f, 'w+b')`, used by PIL)
  can't be written once they exist. It also truncates the stored file without
  truncating handles which are already open on it, which the kernel relies on
  when it sends O_TRUNC as a separate truncate after the open.
  '''
  import io
  import os
  from fsspec.fuse import FUSEr
  class AppyterFUSEr(FUSEr):
    def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self._writers = {} # fh -> path of handles open for writing

    def _fn(self, path):
      return ''.join([self.root, path.lstrip('/')])

    def create(self, path, flags, fi=None):
      fh = super().create(path, flags, fi)
      self._writers[fh] = self._fn(path)
      return fh

    def open(self, path, flags):
      logger.debug(f"open {path} {oct(flags)}")
      fn = self._fn(path)
      access = flags & os.O_ACCMODE
      if access == os.O_RDONLY:
        f = self.fs.open(fn, 'rb')
      elif flags & os.O_APPEND:
        f = self.fs.open(fn, 'ab')
      elif flags & os.O_TRUNC:
        f = self.fs.open(fn, 'wb')
      else:
        # the kernel usually sends O_TRUNC as a separate truncate after the open,
        #  so we must preserve the existing contents for in-place edits;
        #  filesystems which can't do that fall back to overwriting the file
        try:
          f = self.fs.open(fn, 'rb+')
        except (ValueError, NotImplementedError, io.UnsupportedOperation, PermissionError):
          f = self.fs.open(fn, 'wb')
      fh = self.counter
      self.cache[fh] = f
      self.counter += 1
      if access != os.O_RDONLY:
        self._writers[fh] = fn
      return fh

    def truncate(self, path, length, fh=None):
      logger.debug(f"truncate {path} {length} {fh}")
      fn = self._fn(path)
      writers = [self.cache[h] for h, p in self._writers.items() if p == fn and h in self.cache]
      if writers:
        # the open handles get committed when they're released, so they must be truncated
        for f in writers:
          f.truncate(length)
      elif length == 0:
        self.fs.touch(fn)
      else:
        with self.fs.open(fn, 'rb+') as f:
          f.truncate(length)

    def release(self, path, fh):
      self._writers.pop(fh, None)
      return super().release(path, fh)
  return AppyterFUSEr

def _fuse_run(fs_json, fs_path, mount_dir):
  import fsspec.fuse
  import appyter.ext.fsspec
  import appyter.ext.asyncio.event_loop
  from appyter.ext.asyncio.event_loop import with_event_loop
  from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem
  # a forked process inherits the parent's event loop but not the thread running it,
  #  so we start our own
  appyter.ext.asyncio.event_loop._LOOP = None
  with with_event_loop():
    fs = ComposableAbstractFileSystem.from_json(fs_json)
    logger.debug(f'preparing {fs}..')
    with fs as fs:
      logger.debug('launching fuse..')
      fsspec.fuse.run(fs, fs_path, mount_dir, ops_class=_fuser_class())
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
