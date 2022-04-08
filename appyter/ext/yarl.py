import re
import functools
import dataclasses
from yarl import URL
from appyter.ext.pathlib.chroot import ChrootPurePosixPath

def expand_dotmap(query_map):
  ''' Convert dot-notation querystring into option params
  '''
  from appyter.ext.json import try_json_loads
  params = {}
  for K, v in query_map.items():
    _params_n_2 = None
    _params_n_1 = params
    for k in K.split('.'):
      if k not in _params_n_1: _params_n_1[k] = {}
      _params_n_2 = _params_n_1
      _params_n_1 = _params_n_2[k]
    _params_n_2[k] = True if v == '' else try_json_loads(v)
  return params

@dataclasses.dataclass(frozen=True)
class URLEx:
  ''' Extend yarl's URL class with:
  - support for `::` notation as used in fsspec URIs
  - posix_path path operation
  - fragment parsing
  - dotmap support (query_ex)
  '''
  url: URL

  def __init__(self, url):
    if type(url) == str:
      url_split = str(url).split('::')
      url = URL(url_split[-1])
      if url.scheme:
        url = url.with_scheme('::'.join(url_split[:-1] + [url.scheme]))
    elif isinstance(url, URL):
      pass
    elif isinstance(url, URLEx):
      url = url.url
    #
    object.__setattr__(self, 'url', url)

  @property
  def fragment_url(self):
    return URLEx(self.url.fragment)

  @property
  def posix_path(self):
    return ChrootPurePosixPath(self.url.path)

  def join(self, *parts):
    return self.with_path(str(self.posix_path.join(*parts).realpath()))

  @property
  def query_ex(self):
    return expand_dotmap(self.url.query)

  def __getattr__(self, attr):
    '''
    with_/update_ => result in a new URLEx object
    fragment_ => access/update the fragment of the url specifically
    '''
    m = re.match(r'^(with_|update_|)(fragment_)?(.+)$', attr)
    if m:
      if m.group(2):
        if m.group(1):
          with_func_ = getattr(self.fragment_url, m.group(1)+m.group(3))
          @functools.wraps(with_func_)
          def with_(*args, **kwargs):
            return URLEx(self.url.with_fragment(str(with_func_(*args, **kwargs))))
          return with_
        else:
          return getattr(self.fragment_url, m.group(2))
      else:
        if m.group(1):
          with_func_ = getattr(self.url, m.group(0))
          @functools.wraps(with_func_)
          def with_(*args, **kwargs):
            return URLEx(with_func_(*args, **kwargs))
          return with_
        else:
          return getattr(self.url, m.group(0))
    else:
      raise AttributeError

  @classmethod
  def build(fragment=None, fragment_path=None, fragment_query_string=None, fragment_query=None, **kwargs):
    return URLEx(
      URL.build(
        fragment=fragment if fragment is not None else str(URL.build(path=fragment_path, query_string=fragment_query_string, query=fragment_query)),
        **kwargs,
      )
    )
