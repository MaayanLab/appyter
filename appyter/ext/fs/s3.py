import s3fs
import urllib.parse

class Filesystem:
  def __init__(self, uri):
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
  #
  def path(self):
    return None
  #
  def open(self, path, mode='r'):
    return self._fs.open(self._prefix + path, mode=mode)
  #
  def exists(self, path):
    return self._fs.exists(self._prefix + path)
  #
  def makedirs(self, path, exist_ok=False):
    return self._fs.makedirs(self._prefix + path, exist_ok=exist_ok)
  #
  def cp(self, src, dst):
    return self._fs.copy(self._prefix + src, self._prefix + dst, recursive=True)
  #
  def link(self, src, dst):
    print('WARNING: s3 does not support links, copying')
    return self._fs.copy(self._prefix + src, self._prefix + dst, recursive=True)
  #
  def rm(self, path, recursive=False):
    return self._fs.rm(self._prefix + path, recursive=recursive)
  #
  def chmod_ro(self, path):
    print('WARNING: s3 does not support chmod')
    pass
  #
  def __exit__(self, *args):
    pass
