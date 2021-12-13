import re
import itertools
import urllib.parse
from dataclasses import dataclass

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
    K, eq, v = Kv.partition('=')
    if not eq: v = True
    _params_n_2 = None
    _params_n_1 = params
    for k in K.split('.'):
      if k not in _params_n_1: _params_n_1[k] = {}
      _params_n_2 = _params_n_1
      _params_n_1 = _params_n_2[k]
    _params_n_2[k] = try_json_loads(urllib.parse.unquote(v)) if type(v) == str else v
  return params

@dataclass
class URIParsed:
  url: str
  query: str
  fragment: str
  fragment_query: str

  @property
  def qs(self):
    if not self.query: return None
    return parse_qs(self.query)

  @property
  def fragment_qs(self):
    if not self.fragment_query: return None
    return parse_qs(self.fragment_query)

  def __str__(self):
    out = self.url
    if self.query:
      out += '?' + self.query
    if self.fragment:
      out += '#' + self.fragment
      if self.fragment_query:
        out += '?' + self.fragment_query
    elif self.fragment_query:
      out += '#?' + self.fragment_query
    return out

uri_re = re.compile(r'^(?P<url>[^\?#]+)(\?(?P<query>[^#]*))?(#(?P<fragment>[^\?]*?))?(\?(?P<fragment_query>.*?))?$')

def parse_file_uri(uri):
  return URIParsed(**uri_re.match(uri).groupdict())
