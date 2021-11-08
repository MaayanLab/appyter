import itertools
import urllib.parse

from appyter.ext.pathlib.chroot import ChrootPurePosixPath
from appyter.ext.json import try_json_loads

def parent_url(url):
  parent, *filename = url.rsplit('/', maxsplit=1)
  return parent if filename else ''

def join_slash(*parts):
  if not parts: return ''
  part0, *parts = parts
  return '/'.join(itertools.chain((part0.rstrip('/'),), (part.lstrip('/') for part in parts)))

def join_url(root, *parts):
  return join_slash(root, str(ChrootPurePosixPath('/').join(*parts)))

def parse_qs(qs):
  ''' Convert dot-notation querystring into option params
  '''
  params = {}
  for Kv in qs.split('&'):
    K, v = Kv.split('=')
    _params_n_2 = None
    _params_n_1 = params
    for k in K.split('.'):
      if k not in _params_n_1: _params_n_1[k] = {}
      _params_n_2 = _params_n_1
      _params_n_1 = _params_n_2[k]
    _params_n_2[k] = try_json_loads(urllib.parse.unquote(v))
  return params
