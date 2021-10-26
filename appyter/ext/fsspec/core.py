import logging
logger = logging.getLogger(__name__)

from fsspec.core import url_to_fs, split_protocol

def url_to_chroot_fs(url, pathmap=None, **kwargs):
  ''' Like url_to_fs but supporting our extensions, namely:
  chroot   filesystem path is treated as the root
  pathmap  overlay other fsspec-compatible paths
  '''
  if 'file' not in kwargs: kwargs['file'] = {}
  if 'auto_mkdir' not in kwargs['file']: kwargs['file']['auto_mkdir'] = True
  protocol, path = split_protocol(url)
  full_url = 'chroot::' + (protocol or 'file') + '://' + path
  if pathmap is not None:
    full_url = 'pathmap::' + full_url
    kwargs['pathmap'] = dict(pathmap=pathmap)
  fs, _ = url_to_fs(full_url, **kwargs)
  return fs
