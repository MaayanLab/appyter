import tempfile
import urllib.parse
import json
import re
import os
from appyter.ext.fs.file import Filesystem as FSFilesystem


def sh(cmd):
  from subprocess import Popen, PIPE
  return Popen(cmd, stdout=PIPE)

def slugify(s):
  return re.compile(r'[^a-zA-Z0-9-]+').replace(s, '')

class RcloneParse:
  @staticmethod
  def get(scheme):
    return getattr(RcloneParse, '_{}'.format(scheme))

  @staticmethod
  def s3(uri):
    config = dict(urllib.parse.parse_qsl(uri.query))
    if 'env_auth' not in config:
      config['env_auth'] = False
    #
    if 'provider' not in config:
      if uri.hostname.endswith('s3.amazonaws.com'):
        config['provider'] = 'AWS'
      else:
        config['provider'] = 'minio'
    #
    if 'endpoint' not in config:
      if config['provider'] != 'AWS':
        config['endpoint'] = uri.hostname
    #
    if uri.username:
      config['access_key_id'] = uri.username
    if uri.password:
      config['secret_access_key'] = uri.password
    #
    return [el for key, value in config.items() for el in [key, value]]

class Filesystem(FSFilesystem):
  def __init__(self, uri):
    self._uri = uri
    self._scheme = '+'.join(scheme for scheme in self._uri.scheme.split('+') if scheme != 'rclone')
    self._remote = slugify(f"{self._scheme}:{self._uri.hostname}{self._uri.path}?{self._uri.query}")
    if self._remote not in json.load(sh(['rclone', 'config', 'dump']).stdout).keys():
      sh([
        'rclone', 'config', 'create', self._remote, self._scheme,
      ] + RcloneParse.get(self._scheme)(self._uri))
    self._tmpdir = tempfile.mkdtemp()
    self._mount = sh([
      'rclone', 'mount', f"{self._remote}:{self._uri.path[1:]}", self._tmpdir,
    ])
    super().__init__(urllib.parse.urlparse('file://' + self._tmpdir))
  #
  def __exit__(self, *args):
    self.close()
  #
  def link(self, src, dst):
    if self._scheme == 's3':
      print('WARNING: s3 does not support links, copying')
      return self.cp(src, dst, recursive=True)
    return super().link(src, dst)
  #
  def close(self):
    self._mount.terminate()
    self._mount.wait()
    os.rmdir(self._tmpdir)