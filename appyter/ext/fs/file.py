import os
import glob
import shutil
import urllib.parse
import logging
import traceback
logger = logging.getLogger(__name__)

from appyter.ext.fs import Filesystem as FS


class Filesystem:
  def __init__(self, uri):
    self._uri = uri
    self._prefix = self._uri.path
  #
  def __enter__(self):
    return self
  #
  def path(self, path=''):
    return FS.join(self._prefix, path)
  #
  def close(self):
    pass
  #
  def open(self, path, mode='r'):
    try:
      assert path
      if mode[0] in {'w', 'a'}:
        os.makedirs(os.path.dirname(FS.join(self._prefix, path)), exist_ok=True)
      return open(FS.join(self._prefix, path), mode=mode)
    except FileNotFoundError:
      raise Exception(f"No such file or directory: {path}")
    except Exception:
      logger.error(traceback.format_exc())
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def exists(self, path):
    try:
      assert path
      return os.path.isfile(FS.join(self._prefix, path)) or os.path.islink(FS.join(self._prefix, path))
    except Exception:
      logger.error(traceback.format_exc())
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def glob(self, path=''):
    ls_path = FS.join(self._prefix, path) if path else self._prefix
    return [
      f[len(self._prefix)+1:]
      for f in glob.glob(ls_path, recursive=True)
      if os.path.isfile(f)
    ]
  #
  def ls(self, path=''):
    ls_path = FS.join(self._prefix, path) if path else self._prefix
    return [
      f[len(ls_path)+1:]
      for f in glob.glob(ls_path + '/**/*', recursive=True)
      if os.path.isfile(f)
    ]
  #
  def cp(self, src, dst):
    try:
      assert src and dst
      os.makedirs(os.path.dirname(FS.join(self._prefix, dst)), exist_ok=True)
      return shutil.copy(FS.join(self._prefix, src), FS.join(self._prefix, dst))
    except Exception:
      logger.error(traceback.format_exc())
      raise Exception(f"An error occurred while trying to copy {src} to {dst}")
  #
  def link(self, src, dst):
    try:
      assert src and dst
      os.makedirs(os.path.dirname(FS.join(self._prefix, dst)), exist_ok=True)
      return os.link(FS.join(self._prefix, src), FS.join(self._prefix, dst))
    except Exception:
      logger.error(traceback.format_exc())
      raise Exception(f"An error occurred while trying to link {src} to {dst}")
  #
  def rm(self, path, recursive=False):
    try:
      assert path
      if recursive:
        return shutil.rmtree(FS.join(self._prefix, path))
      else:
        return os.remove(FS.join(self._prefix, path))
    except Exception:
      logger.error(traceback.format_exc())
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def chmod_ro(self, path):
    try:
      assert path
      return os.chmod(FS.join(self._prefix, path), 400)
    except Exception:
      logger.error(traceback.format_exc())
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def __exit__(self, *args):
    pass
