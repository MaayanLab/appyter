import s3fs
import urllib.parse

class Filesystem:
  def __init__(self, uri):
    try:
      self._uri = uri
      self._config = {}
      #
      if self._uri.username and self._uri.password:
        self._config['key'] = self._uri.username
        self._config['secret'] = self._uri.password
      elif self._uri.username:
        self._config['token'] = self._uri.username
      else:
        self._config.update(dict(urllib.parse.parse_qsl(self._uri.query)))
      self._config['client_kwargs'] = dict(endpoint_url=f"{'https' if self._config.get('use_ssl') else 'http'}://{self._uri.netloc}")
      self._config['config_kwargs'] = dict(signature_version='s3v4')
      #
      self._prefix = self._uri.path.lstrip('/').rstrip('/') + '/'
      self._fs = s3fs.S3FileSystem(**self._config)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An internal error occurred")
  #
  def path(self):
    return None
  #
  def __enter__(self):
    return self
  #
  def __exit__(self, *args):
    pass
  #
  def close(self):
    pass
  #
  def open(self, path, mode='r'):
    try:
      assert path
      return self._fs.open(self._prefix + path, mode=mode)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def exists(self, path):
    try:
      assert path
      return self._fs.exists(self._prefix + path)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def makedirs(self, path, exist_ok=False):
    try:
      assert path
      return self._fs.makedirs(self._prefix + path, exist_ok=exist_ok)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def cp(self, src, dst):
    try:
      assert src and dst
      return self._fs.copy(self._prefix + src, self._prefix + dst, recursive=True)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to copy {src} to {dst}")
  #
  def link(self, src, dst):
    try:
      assert src and dst
      print('WARNING: s3 does not support links, copying')
      return self._fs.copy(self._prefix + src, self._prefix + dst, recursive=True)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to link {src} to {dst}")
  #
  def rm(self, path, recursive=False):
    try:
      assert path
      return self._fs.rm(self._prefix + path, recursive=recursive)
    except Exception:
      import traceback
      traceback.print_exc()
      raise Exception(f"An error occurred while trying to access {path}")
  #
  def chmod_ro(self, path):
    print('WARNING: s3 does not support chmod')