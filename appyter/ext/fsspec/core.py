import logging

from appyter.ext.fsspec.parse import parse_file_uri_qs
logger = logging.getLogger(__name__)

from fsspec.core import url_to_fs, split_protocol

def url_to_chroot_fs(url, chroot=True, pathmap=None, simplecache=False, **kwargs):
  ''' Like url_to_fs but supporting our extensions, namely:
  chroot       filesystem path is treated as the root
  pathmap      overlay other fsspec-compatible paths
  simplecache  cache read/writes
  '''
  url, qs = parse_file_uri_qs(url)
  protocol, path = split_protocol(url)
  protocol = protocol or 'file'
  full_url = protocol + '://' + path
  if chroot:
    full_url = 'chroot::' + full_url
  # add protocol options to inner protocol
  if protocol not in kwargs: kwargs[protocol] = {}
  kwargs[protocol].update(qs)
  # ensure auto_mkdir is enabled
  if protocol == 'file':
    if 'auto_mkdir' not in kwargs[protocol]: kwargs[protocol]['auto_mkdir'] = True
  # add pathmap as necessary
  if pathmap:
    full_url = 'pathmap::' + full_url
    kwargs['pathmap'] = dict(pathmap=pathmap)
  if simplecache:
    full_url = 'simplecache::' + full_url
  fs, _ = url_to_fs(full_url, **kwargs)
  return fs
