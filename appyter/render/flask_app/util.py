import uuid
import urllib.parse

from appyter.util import join_routes, safe_join, secure_url, secure_filepath

def sha1sum_io(io, chunk_size=65536):
  import hashlib
  sha1 = hashlib.sha1()
  while buf := io.read(chunk_size):
    sha1.update(buf)
  return sha1.hexdigest()

def sha1sum_dict(obj):
  import json, hashlib
  sha1 = hashlib.sha1()
  sha1.update(json.dumps(obj, sort_keys=True, separators=None, ensure_ascii=True).encode())
  return sha1.hexdigest()

def sanitize_sha1sum(val):
  import re
  m = re.match(r'^[0-9a-f]{40}$', val)
  return val if m else None

def generate_uuid():
  return str(uuid.uuid4())

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
