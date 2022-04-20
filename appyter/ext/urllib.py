import re
import itertools
import dataclasses
import typing as t
import urllib.parse
from appyter.ext.pathlib.chroot import ChrootPurePosixPath
from appyter.ext.dict import dict_merge, expand_dotmap

def parent_url(url):
  parent, *filename = url.rsplit('/', maxsplit=1)
  return parent if filename else ''

def url_filename(url):
  parent, *filename = url.rsplit('/', maxsplit=1)
  return filename[0] if filename else parent

def join_slash(*parts):
  if not parts: return ''
  part0, *parts = parts
  return '/'.join(itertools.chain((part0.rstrip('/'),), (part.lstrip('/') for part in parts)))

def join_url(root, *parts):
  return join_slash(root, str(ChrootPurePosixPath('/').join(*parts)))

url_expr = re.compile(
  r'^((?P<scheme>.+?)://(?P<authority>((?P<username>[^/:@\?#]+?)(:(?P<password>[^/@\?#]+?))?@)?(?P<netloc>(?P<hostname>[^:/\?#]+)(:(?P<port>\d+))?))?)?(?P<path>.*?)(\?(?P<query_string>.*?))?(#(?P<fragment>.*?))?$'
)
fragment_expr =  re.compile(
  r'^(?P<path>.*?)(\?(?P<query_string>.*?))?$'
)

def parse_qs_values(query_map):
  from appyter.ext.itertools import collapse
  from appyter.ext.json import try_json_loads
  return {
    k: collapse([try_json_loads(v) if v != '' else True for v in V])
    for k, V in query_map.items()
  }

@dataclasses.dataclass(init=False, repr=False, frozen=True)
class URI:
  ''' Not unlike yarl's URL class but
  - support for `::` notation as used in fsspec URIs
  - posix_path path operation
  - fragment parsing
  - dotmap support (query_ex)
  '''
  scheme: t.Optional[str]
  username: t.Optional[str]
  password: t.Optional[str]
  hostname: t.Optional[str]
  port: t.Optional[int]
  path: str
  query_string: t.Optional[str]
  fragment: t.Optional[str]

  def __init__(self, url=None, scheme=None, username=None, password=None, hostname=None, port=None, path=None, query_string=None, fragment=None):
    if url is not None:
      m = url_expr.match(url)
      object.__setattr__(self, 'scheme', m.group('scheme'))
      object.__setattr__(self, 'username', m.group('username'))
      object.__setattr__(self, 'password', m.group('password'))
      object.__setattr__(self, 'hostname', m.group('hostname'))
      object.__setattr__(self, 'port', int(m.group('port')) if m.group('port') is not None else None)
      object.__setattr__(self, 'path', m.group('path'))
      object.__setattr__(self, 'query_string', m.group('query_string'))
      object.__setattr__(self, 'fragment', m.group('fragment'))
    else:
      object.__setattr__(self, 'scheme', scheme)
      object.__setattr__(self, 'username', username)
      object.__setattr__(self, 'password', password)
      object.__setattr__(self, 'hostname', hostname)
      object.__setattr__(self, 'port', int(port) if port is not None else None)
      object.__setattr__(self, 'path', path or '')
      object.__setattr__(self, 'query_string', query_string)
      object.__setattr__(self, 'fragment', fragment)

  @property
  def netloc(self):
    if self.hostname is not None and self.port is not None:
      return f"{self.hostname}:{self.port}"
    elif self.hostname is not None:
      return self.hostname
    else:
      return None

  @property
  def auth(self):
    if self.username is not None:
      if self.password is not None:
        return f"{self.username}:{self.password}"
      else:
        return self.username
    return None

  @property
  def authority(self):
    if self.netloc is not None:
      if self.auth is not None:
        return f"{self.auth}@{self.netloc}"
      else:
        return self.netloc
    return None

  @property
  def posix_path(self):
    return ChrootPurePosixPath(self.path)

  @property
  def name(self):
    return self.posix_path.root.name

  @property
  def parent(self):
    return self.with_path(str(self.posix_path.root.parent))

  @property
  def query(self):
    return urllib.parse.parse_qs(self.query_string) if self.query_string is not None else None

  @property
  def query_ex(self):
    return expand_dotmap(parse_qs_values(self.query)) if self.query is not None else {}

  @property
  def fragment_path(self):
    return fragment_expr.match(self.fragment).group('path') if self.fragment is not None else None

  @property
  def fragment_posix_path(self):
    return ChrootPurePosixPath(self.fragment_path) if self.fragment_path is not None else None

  @property
  def fragment_name(self):
    return self.fragment_posix_path.root.name if self.fragment_posix_path is not None else None

  @property
  def fragment_parent(self):
    return self.with_path(str(self.fragment_posix_path.root.parent)) if self.fragment_posix_path is not None else None

  @property
  def fragment_query_string(self):
    return fragment_expr.match(self.fragment).group('query_string') if self.fragment is not None else None

  @property
  def fragment_query(self):
    return urllib.parse.parse_qs(self.fragment_query_string) if self.fragment_query_string is not None else None

  @property
  def fragment_query_ex(self):
    return expand_dotmap(parse_qs_values(self.fragment_query)) if self.fragment_query is not None else {}

  def __str__(self):
    return ''.join(filter(None, (
      f"{self.scheme}://" if self.scheme is not None else None,
      join_url(self.authority, self.path) if self.authority is not None else self.path,
      f"?{self.query_string}" if self.query_string is not None else None,
      f"#{self.fragment}" if self.fragment is not None else None,
    )))

  def __repr__(self):
    return "{}('{}')".format(self.__class__.__name__, str(self))

  def with_scheme(self, scheme):
    return URI(
      scheme=scheme,
      username=self.username,
      password=self.password,
      hostname=self.hostname,
      port=self.port,
      path=self.path,
      query_string=self.query_string,
      fragment=self.fragment,
    )

  def with_username(self, username):
    return URI(
      scheme=self.scheme,
      username=username,
      password=self.password,
      hostname=self.hostname,
      port=self.port,
      path=self.path,
      query_string=self.query_string,
      fragment=self.fragment,
    )

  def with_password(self, password):
    return URI(
      scheme=self.scheme,
      username=self.username,
      password=password,
      hostname=self.hostname,
      port=self.port,
      path=self.path,
      query_string=self.query_string,
      fragment=self.fragment,
    )

  def with_hostname(self, hostname):
    return URI(
      scheme=self.scheme,
      username=self.username,
      password=self.password,
      hostname=hostname,
      port=self.port,
      path=self.path,
      query_string=self.query_string,
      fragment=self.fragment,
    )

  def with_port(self, port):
    return URI(
      scheme=self.scheme,
      username=self.username,
      password=self.password,
      hostname=self.hostname,
      port=port,
      path=self.path,
      query_string=self.query_string,
      fragment=self.fragment,
    )

  def with_path(self, path):
    return URI(
      scheme=self.scheme,
      username=self.username,
      password=self.password,
      hostname=self.hostname,
      port=self.port,
      path=path,
      query_string=self.query_string,
      fragment=self.fragment,
    )

  def with_query_string(self, query_string):
    return URI(
      scheme=self.scheme,
      username=self.username,
      password=self.password,
      hostname=self.hostname,
      port=self.port,
      path=self.path,
      query_string=query_string,
      fragment=self.fragment,
    )

  def with_query(self, query):
    return self.with_query_string(urllib.parse.urlencode(query, doseq=True) if query is not None else None)

  def update_query(self, query):
    return self.with_query(dict_merge(self.query or {}, **query))

  def with_fragment(self, fragment):
    return URI(
      scheme=self.scheme,
      username=self.username,
      password=self.password,
      hostname=self.hostname,
      port=self.port,
      path=self.path,
      query_string=self.query_string,
      fragment=fragment,
    )

  def with_fragment_path(self, fragment_path):
    if fragment_path is None and self.fragment_query_string is None:
      return self.with_fragment(None)
    elif self.fragment_query_string is None:
      return self.with_fragment(fragment_path)
    else:
      return self.with_fragment(f"{fragment_path or ''}?{self.fragment_query_string}")

  def with_fragment_query_string(self, fragment_query_string):
    if self.fragment_path is None and fragment_query_string is None:
      return self.with_fragment(None)
    elif fragment_query_string is None:
      return self.with_fragment(self.fragment_path)
    else:
      return self.with_fragment(f"{self.fragment_path or ''}?{fragment_query_string}")

  def with_fragment_query(self, fragment_query):
    return self.with_fragment_query_string(urllib.parse.urlencode(fragment_query, doseq=True))

  def update_fragment_query(self, fragment_query):
    return self.with_fragment_query(dict_merge(self.fragment_query or {}, **fragment_query))

  def join(self, *parts):
    return self.with_path(str(self.posix_path.join(*parts).realpath())) if self.posix_path is not None else None

  def fragment_join(self, *parts):
    return self.with_fragment_path(str(self.fragment_posix_path.join(*parts).realpath())) if self.fragment_posix_path is not None else None
