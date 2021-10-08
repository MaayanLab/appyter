import sys
import yaml
import tempfile
import urllib.parse
import os
import time
import logging
logger = logging.getLogger(__name__)

from appyter.ext.fs import Filesystem as FS
from appyter.ext.fs.file import Filesystem as FSFilesystem


def sh(cmd, _in=None):
  from subprocess import Popen, PIPE
  kwargs = dict(stdout=PIPE)
  if _in is not None:
    kwargs['stdin'] = PIPE
  proc = Popen(cmd, **kwargs)
  if _in is not None:
    proc.stdin.write(_in.encode())
    proc.stdin.close()
  return proc

def quote(s, double=False):
  if double:
    return '"' + s.replace('"', '""') + '"'
  else:
    return "'" + s.replace("'", "''") + "'"

def sync_async_sleep(amnt, asynchronous=False):
  if asynchronous:
    import asyncio
    asyncio.ensure_future(asyncio.sleep(amnt))
  else:
    time.sleep(amnt)

class RCloneParseS3:
  def __init__(self, uri):
    self.uri = uri
    self.config = dict(urllib.parse.parse_qsl(self.uri.query))
    if 'env_auth' not in self.config:
      self.config['env_auth'] = 'false'
    #
    if 'provider' not in self.config:
      if self.uri.hostname.endswith('s3.amazonaws.com'):
        self.config['provider'] = 'AWS'
      else:
        self.config['provider'] = 'Minio'
    #
    if 'endpoint' not in self.config:
      if self.config['provider'] != 'AWS':
        self.config['endpoint'] = f"{'https' if self.config.get('use_ssl') else 'http'}://{self.uri.hostname}"
        if self.uri.port:
          self.config['endpoint'] += f":{self.uri.port}"
    #
    if self.uri.username:
      self.config['access_key_id'] = self.uri.username
    if self.uri.password:
      self.config['secret_access_key'] = self.uri.password
  def __str__(self):
    return f":s3,{','.join([f'{key}={quote(value)}' for key, value in self.config.items()])}:{self.uri.path[1:]}"

class RCloneParseHttp:
  def __init__(self, uri):
    self.uri = uri
  def __str__(self):
    return f":http,url={quote(self.uri.geturl())}"

class RCloneParseFtp:
  def __init__(self, uri):
    self.uri = uri
    self.config = dict(host=self.uri.hostname)
    if self.uri.port:
      self.config['port'] = str(self.uri.port)
    if self.uri.username:
      self.config['user'] = str(self.uri.username)
    if self.uri.password:
      self.config['pass'] = str(self.uri.password)
  def __str__(self):
    return f":ftp,{','.join([f'{key}={quote(value)}' for key, value in self.config.items()])}:{self.uri.path[1:]}"

class RCloneParseFile:
  def __init__(self, uri) -> None:
    self.uri = uri
  def __str__(self):
    return self.uri.path

class RCloneParse:
  lookup = {
    'storage': lambda uri: RCloneParse(
      FS.join(FS('storage:///').uri.geturl(), '.'+uri.path)
    ),
    's3': RCloneParseS3,
    'rclone+s3': RCloneParseS3,
    'http': RCloneParseHttp,
    'ftp': RCloneParseFtp,
    'file': RCloneParseFile,
  }
  def __new__(self, uri):
    logger.debug(uri)
    uri = urllib.parse.urlparse(uri) if type(uri) == str else uri
    return RCloneParse.lookup[uri.scheme](uri)

class Filesystem(FSFilesystem):
  def __init__(self, uri, pathmap={}, asynchronous=False, **kwargs):
    logger.debug(pathmap)
    self.uri = uri
    self._scheme = '+'.join(scheme for scheme in uri.scheme.split('+') if scheme != 'rclone')
    self._remote = str(RCloneParse(uri))
    self._tmpdir = tempfile.mkdtemp()
    logger.debug(f"Mounting {self._remote} on {self._tmpdir}")
    rclone_pathmap = {
      f"/{k}": str(RCloneParse(v))
      for k, v in pathmap.items()
    }
    logger.debug(rclone_pathmap)
    self._mount = sh([
      sys.executable, '-u', '-m', 'rclone_pathmap', 'mount',
      '-c', '-', self._remote, self._tmpdir,
      '--vfs-cache-mode', 'writes',
    ], _in=yaml.dump(rclone_pathmap))
    sync_async_sleep(0.1, asynchronous=asynchronous)
    while not os.path.ismount(self._tmpdir):
      if self._mount.poll() is not None:
        raise Exception(f"Mount exited with code {self._mount.returncode} before mounting")
      sync_async_sleep(0.1, asynchronous=asynchronous)
    super().__init__(urllib.parse.urlparse('file://' + self._tmpdir))
  #
  def __exit__(self, *args):
    self.close()
  #
  def link(self, src, dst):
    if self._scheme == 's3':
      logger.info('WARNING: s3 does not support links, copying')
      return self.cp(src, dst)
    return super().link(src, dst)
  #
  def close(self):
    logger.debug('Unmounting...')
    self._mount.terminate()
    self._mount.wait()
    os.rmdir(self._tmpdir)
