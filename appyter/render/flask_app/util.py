import uuid
import urllib.parse

from appyter.util import join_routes, secure_filename

def sanitize_uuid(val):
  try:
    return str(uuid.UUID(val))
  except:
    return None

def collapse(L):
  if len(L) == 1:
    return L[0]
  else:
    return L

def secure_url(url):
  parsed = urllib.parse.urlparse(url)
  assert parsed.scheme in {'https', 'http', 'ftp'}, 'Invalid scheme'
  return url

def route_join_with_or_without_slash(blueprint, *routes, **kwargs):
  ''' Like @app.route but doesn't care about trailing slash or not
  '''
  def wrapper(func):
    routes_stripped = join_routes(*routes)
    if routes_stripped:
      blueprint.route(routes_stripped, **kwargs)(func)
    blueprint.route(routes_stripped + '/', **kwargs)(func)
    return func
  return wrapper
