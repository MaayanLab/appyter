import os
import shutil
import urllib.parse

class Filesystem:
  def __init__(self, uri):
    self._uri = uri
    self._prefix = self._uri.path
  #
  def __enter__(self):
    return self
  #
  def open(self, path, mode='r'):
    return open(os.path.join(self._prefix, path), mode=mode)
  #
  def exists(self, path):
    return os.path.exists(os.path.join(self._prefix, path))
  #
  def makedirs(self, path, exist_ok=False):
    return os.makedirs(os.path.join(self._prefix, path), exist_ok=exist_ok)
  #
  def link(self, src, dst):
    return os.link(os.path.join(self._prefix, src), os.path.join(self._prefix, dst))
  #
  def rm(self, path, recursive=False):
    if recursive:
      return shutil.rmtree(os.path.join(self._prefix, path))
    else:
      return os.remove(os.path.join(self._prefix, path))
  #
  def chmod_ro(self, path):
    return os.chmod(os.path.join(self._prefix, path), 400)
  #
  def __exit__(self, *args):
    pass
