import uuid
import urllib.parse

from appyter.util import join_routes, secure_filename, secure_url

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
