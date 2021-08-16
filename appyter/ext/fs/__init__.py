import os
import shutil
import importlib
import urllib.parse
from werkzeug.security import safe_join

class Filesystem:
  def __init__(self, uri, with_path=False, asynchronous=False):
    if '://' not in uri:
      uri = 'file://' + uri
    uri_parsed = urllib.parse.urlparse(uri)
    self._fs = None
    if uri_parsed.scheme == 'file':
      from appyter.ext.fs.file import Filesystem as FSFilesystem
      self._fs = FSFilesystem(uri_parsed)
    if uri_parsed.scheme == 'tmpfs':
      from appyter.ext.fs.tmpfs import Filesystem as TmpFilesystem
      self._fs = TmpFilesystem(uri_parsed)
    if uri_parsed.scheme == 's3':
      if not with_path:
        from appyter.ext.fs.s3 import Filesystem as S3Filesystem
        self._fs = S3Filesystem(uri_parsed, asynchronous=asynchronous)
      else:
        # we will need rclone to do s3 mounting with_path
        uri_parsed = uri_parsed._replace(scheme='s3+rclone')
    if 'rclone' in uri_parsed.scheme.split('+'):
      from appyter.ext.fs.rclone import Filesystem as RcloneFilesystem
      self._fs = RcloneFilesystem(uri_parsed, asynchronous=asynchronous)
    #
    if self._fs is None:
      raise Exception(f"Unrecognized scheme {uri}")
  #
  def __enter__(self):
    return self._fs.__enter__()
  #
  def path(self, path=''):
    return self._fs.path(path)
  #
  def close(self):
    return self._fs.close()
  #
  def open(self, path, mode='r'):
    return self._fs.open(path, mode=mode)
  #
  def exists(self, path):
    return self._fs.exists(path)
  #
  def glob(self, path=''):
    return self._fs.glob(path=path)
  #
  def ls(self, path=''):
    return self._fs.ls(path=path)
  #
  def cp(self, src, dst):
    return self._fs.cp(src, dst)
  #
  def link(self, src, dst):
    return self._fs.link(src, dst)
  #
  def rm(self, path, recursive=False):
    return self._fs.rm(path, recursive=recursive)
  #
  def chmod_ro(self, path):
    return self._fs.chmod_ro(path)
  #
  def __exit__(self, *args):
    return self._fs.__exit__(*args)
  #
  @staticmethod
  def join(*args):
    return safe_join(*args)
  #
  @staticmethod
  def cp(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    if src_fs == dst_fs:
      src_fs.cp(src_path, dst_path)
    else:
      with src_fs.open(src_path, 'rb') as fr:
        with dst_fs.open(dst_path, 'wb') as fw:
          shutil.copyfileobj(fr, fw)
  #
  @staticmethod
  def mv(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    if src_fs == dst_fs:
      src_fs.mv(src_path, dst_path)
    else:
      Filesystem.cp(src_fs=src_fs, src_path=src_path, dst_fs=dst_fs, dst_path=dst_path)
      src_fs.rm(src_path)
  #
