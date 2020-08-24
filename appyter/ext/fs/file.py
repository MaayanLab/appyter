import os
import shutil
import urllib.parse
from appyter.ext.fs import Filesystem as FS

class Filesystem:
  def __init__(self, uri):
    self._uri = uri
    self._prefix = self._uri.path
  #
  def __enter__(self):
    return self
  #
  def path(self):
    return self._prefix
  #
  def open(self, path, mode='r'):
    try:
      return open(FS.join(self._prefix, path), mode=mode)
    except FileNotFoundError:
      raise Exception('No such file or directory: {path}')
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def exists(self, path):
    try:
      return os.path.isfile(FS.join(self._prefix, path)) or os.path.islink(FS.join(self._prefix, path))
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def makedirs(self, path, exist_ok=False):
    try:
      return os.makedirs(FS.join(self._prefix, path), exist_ok=exist_ok)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def cp(self, src, dst):
    try:
      return shutil.copy(FS.join(self._prefix, src), FS.join(self._prefix, dst))
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def link(self, src, dst):
    try:
      return os.link(FS.join(self._prefix, src), FS.join(self._prefix, dst))
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def rm(self, path, recursive=False):
    try:
      if recursive:
        return shutil.rmtree(FS.join(self._prefix, path))
      else:
        return os.remove(FS.join(self._prefix, path))
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def chmod_ro(self, path):
    try:
      return os.chmod(FS.join(self._prefix, path), 400)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def __exit__(self, *args):
    pass
