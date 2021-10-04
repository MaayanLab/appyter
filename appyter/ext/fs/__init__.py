import shutil
import importlib
import urllib.parse
from werkzeug.security import safe_join

class Filesystem:
  protocols = {
    'file': lambda *args, **kwargs: importlib.import_module('appyter.ext.fs.file').Filesystem(*args, **kwargs),
    'tmpfs': lambda *args, **kwargs: importlib.import_module('appyter.ext.fs.tmpfs').Filesystem(*args, **kwargs),
    's3': lambda *args, **kwargs: importlib.import_module('appyter.ext.fs.s3').Filesystem(*args, **kwargs),
    'rclone+s3': lambda *args, **kwargs: importlib.import_module('appyter.ext.fs.rclone').Filesystem(*args, **kwargs),
  }
  def __init__(self, uri, root=None, **kwargs):
    if '://' not in uri:
      uri = 'file://' + uri
    self._uri = uri
    self._root = self if root is None else root
    self._kwargs = kwargs
    uri_parsed = urllib.parse.urlparse(uri)
    self._fs = Filesystem.protocols[uri_parsed.scheme](uri_parsed, **kwargs)
    self._fs._root = self._root
  #
  def __enter__(self):
    return self._fs.__enter__()
  #
  def chroot(self, subpath, **kwargs):
    return Filesystem(Filesystem.join(self._uri, f".{subpath}"), root=self._root, **kwargs)
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
  def gcd(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    ''' Greatest common denominator file path, useful for
    optimizing staticmethods when filesystems overlap with one another
    '''
    if len(src_fs._root._uri) < len(dst_fs._root._uri):
      if src_fs._root._uri == dst_fs._root._uri[:len(src_fs._root._uri)]:
        return src_fs._root, src_path, Filesystem.join(dst_fs._root[len(src_fs._root._uri):], dst_path)
    else:
      if dst_fs._root._uri == src_fs._root._uri[:len(dst_fs._root._uri)]:
        return dst_fs._root, Filesystem.join(src_fs[len(dst_fs._root._uri):], src_path), dst_path
  #
  @staticmethod
  def join(*args):
    return safe_join(*args)
  #
  @staticmethod
  def link(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    fs_src_dst = Filesystem.gcd(src_fs=src_fs, src_path=src_path, dst_fs=dst_fs, dst_path=dst_path)
    if fs_src_dst:
      fs, src, dst = fs_src_dst
      fs.link(src, dst)
    else:
      with src_fs.open(src_path, 'rb') as fr:
        with dst_fs.open(dst_path, 'wb') as fw:
          shutil.copyfileobj(fr, fw)
  #
  @staticmethod
  def cp(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    fs_src_dst = Filesystem.gcd(src_fs, src_path, dst_fs, dst_path)
    if fs_src_dst:
      fs, src, dst = fs_src_dst
      fs.cp(src, dst)
    else:
      with src_fs.open(src_path, 'rb') as fr:
        with dst_fs.open(dst_path, 'wb') as fw:
          shutil.copyfileobj(fr, fw)
  #
  @staticmethod
  def mv(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    fs_src_dst = Filesystem.gcd(src_fs, src_path, dst_fs, dst_path)
    if fs_src_dst:
      fs, src, dst = fs_src_dst
      fs.mv(src, dst)
    else:
      Filesystem.cp(src_fs=src_fs, src_path=src_path, dst_fs=dst_fs, dst_path=dst_path)
      src_fs.rm(src_path)
  #
