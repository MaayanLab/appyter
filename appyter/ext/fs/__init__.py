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
  def __new__(self, uri, **kwargs):
    if '://' not in uri:
      uri = 'file://' + uri
    uri = urllib.parse.urlparse(uri)
    return Filesystem.protocols[uri.scheme](uri, **kwargs)
  #
  @staticmethod
  def chroot(fs, subpath, **kwargs):
    return Filesystem(
      Filesystem.join(fs.uri.geturl(), subpath.lstrip('/')),
      **kwargs
    )
  #
  @staticmethod
  def gcd(src_fs=None, src_path=None, dst_fs=None, dst_path=None):
    ''' Greatest common denominator file path, useful for
    optimizing staticmethods when filesystems overlap with one another
    '''
    # TODO: optimize other schemes
    if src_fs.uri.scheme == 'file' and dst_fs.uri.scheme == 'file':
      from pathlib import PurePosixPath
      if PurePosixPath(src_fs.uri.path).is_relative_to(dst_fs.uri.path):
        return Filesystem(f"file://{dst_fs.uri.path}"), (PurePosixPath(src_fs.uri.path) / src_path).relative_to(dst_fs.uri.path), dst_path
      elif PurePosixPath(dst_fs.uri.path).is_relative_to(src_fs.uri.path):
        return Filesystem(f"file://{src_fs.uri.path}"), src_path, (PurePosixPath(dst_fs.uri.path) / dst_path).relative_to(src_fs.uri.path)
      else:
        src_parts = PurePosixPath(src_fs.uri.path).parts
        dst_parts = PurePosixPath(dst_fs.uri.path).parts
        common_parts = []
        for src_part, dst_part in zip(src_parts, dst_parts):
          if src_part == dst_part:
            common_parts.append(src_part)
          else:
            break
        common_path = PurePosixPath('/' + '/'.join(common_parts[1:]))
        return Filesystem(f"file://{str(common_path)}"), (PurePosixPath(src_fs.uri.path) / src_path).relative_to(common_path), (PurePosixPath(dst_fs.uri.path) / dst_path).relative_to(common_path)
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
