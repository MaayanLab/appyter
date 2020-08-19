import uuid
import urllib.parse

from appyter.util import join_routes, secure_filename, secure_url

def sha1sum_file(filename, chunk_size=65536):
  import hashlib
  sha1 = hashlib.sha1()
  with open(filename, 'rb') as fr:
    while buf := fr.read(chunk_size):
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

def route_join_with_or_without_slash(blueprint, *routes, redirect_slash=False, **kwargs):
  ''' Like @app.route but doesn't care about trailing slash or not
  '''
  def wrapper(func):
    routes_stripped = join_routes(*routes)
    routed_func = blueprint.route(routes_stripped + '/', **kwargs)(func)
    if routes_stripped:
      if redirect_slash:
        @blueprint.route(routes_stripped, **kwargs)
        def _():
          from flask import redirect, url_for
          return redirect(url_for(routed_func))
      else:
        return blueprint.route(routes_stripped, **kwargs)(routed_func)
    return routed_func
  return wrapper
