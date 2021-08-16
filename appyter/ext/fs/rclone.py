import tempfile
import urllib.parse
import json
import re
import os
import time
import logging
logger = logging.getLogger(__name__)

from appyter.ext.fs.file import Filesystem as FSFilesystem


def sh(cmd):
  from subprocess import Popen, PIPE
  return Popen(cmd, stdout=PIPE)

def slugify(s):
  return re.sub(r'[^a-zA-Z0-9-]+', '', s)

def sync_async_sleep(amnt, asynchronous=False):
  if asynchronous:
    import asyncio
    asyncio.ensure_future(asyncio.sleep(amnt))
  else:
    time.sleep(amnt)

class RcloneParse:
  @staticmethod
  def get(scheme):
    return getattr(RcloneParse, '_{}'.format(scheme))

  @staticmethod
  def _s3(uri):
    config = dict(urllib.parse.parse_qsl(uri.query))
    if 'env_auth' not in config:
      config['env_auth'] = 'false'
    #
    if 'provider' not in config:
      if uri.hostname.endswith('s3.amazonaws.com'):
        config['provider'] = 'AWS'
      else:
        config['provider'] = 'Minio'
    #
    if 'endpoint' not in config:
      if config['provider'] != 'AWS':
        config['endpoint'] = f"{'https' if config.get('use_ssl') else 'http'}://{uri.hostname}"
        if uri.port:
          config['endpoint'] += f":{uri.port}"
    #
    if uri.username:
      config['access_key_id'] = uri.username
    if uri.password:
      config['secret_access_key'] = uri.password
    #
    return [el for key, value in config.items() for el in [key, value]]

class Filesystem(FSFilesystem):
  def __init__(self, uri, asynchronous=False):
    self._uri = uri
    self._scheme = '+'.join(scheme for scheme in self._uri.scheme.split('+') if scheme != 'rclone')
    self._remote = slugify(f"{self._scheme}:{self._uri.hostname}{self._uri.path}?{self._uri.query}")
    if self._remote not in json.load(sh(['rclone', 'config', 'dump']).stdout).keys():
      if sh(['rclone', 'config', 'create', self._remote, self._scheme] + RcloneParse.get(self._scheme)(self._uri)).wait() != 0:
        raise Exception('Error configuring rclone')
    self._tmpdir = tempfile.mkdtemp()
    logger.debug(f"Mounting {self._remote}:{self._uri.path[1:]} on {self._tmpdir}")
    self._mount = sh([
      'rclone', 'mount', '--vfs-cache-mode', 'writes', f"{self._remote}:{self._uri.path[1:]}", self._tmpdir,
    ])
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
