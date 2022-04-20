import logging
import functools
import urllib.parse
from werkzeug.security import safe_join

from appyter.ext.itertools import collapse

logger = logging.getLogger(__name__)

def join_routes(*routes):
  ''' Utility function for joining routes while striping extraneous slashes
  '''
  return '/' + '/'.join([route.strip('/') for route in routes if route.strip('/')])

def secure_filepath(filepath):
  ''' Ensures this will be a sanitized relative path
  '''
  secured_filepath = safe_join('.', filepath.lstrip('/'))
  assert secured_filepath is not None, "Filepath wasn't secure"
  secured_filepath = secured_filepath[2:]
  if not secured_filepath:
    logger.debug("Filepath became empty while securing")
    return ''
  return secured_filepath

def secure_url(url):
  parsed = urllib.parse.urlparse(url)
  assert parsed.scheme in {'https', 'http', 'ftp'}, 'Invalid scheme'
  return url

def is_remote(url):
  try:
    secure_url(url)
    return True
  except AssertionError:
    return False

def request_get(request, key, default=None):
  if type(request) == dict:
    return request.get(key) if key in request else default
  elif getattr(request, 'method', None) is not None:
    if request.method == 'GET':
      return collapse(request.args.getlist(key)) if key in request.args else default
    elif request.is_json:
      return request.json.get(key) if key in request.json else default
    else:
      return collapse(request.form.getlist(key)) if key in request.form else default
  else:
    raise NotImplementedError

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

def decorator_in_production(production_decorator):
  def decorator(func):
    production_func = production_decorator(func)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
      try:
        from flask import current_app
        if current_app.config['DEBUG']:
          return func(*args, **kwargs)
      except RuntimeError:
        pass
      return production_func(*args, **kwargs)
    return wrapper
  return decorator
