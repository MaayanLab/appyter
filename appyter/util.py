import json
import logging
import functools
import urllib.parse
from werkzeug.security import safe_join

logger = logging.getLogger(__name__)

def dict_filter_none(d):
  return { k: v for k, v in d.items() if v }

def join_routes(*routes):
  ''' Utility function for joining routes while striping extraneous slashes
  '''
  return '/' + '/'.join([route.strip('/') for route in routes if route.strip('/')])

def re_full(expr):
  if not expr.startswith('^'): expr = '^' + expr
  if not expr.endswith('$'): expr = expr + '$'
  return expr

def secure_filepath(filepath):
  ''' Ensures this will be a sanitized relative path
  '''
  secured_filepath = safe_join('.', filepath)
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
  except:
    return False

def importdir(_dirname_, _package_, _globals_):
  import os, importlib
  for f in os.listdir(_dirname_):
    if f.startswith('_') or f.startswith('.'):
      continue
    if f.endswith('.py'):
      modname = f[:-len('.py')]
    elif os.path.isdir(os.path.join(_dirname_, f)):
      modname = f
    else:
      continue
    mod = importlib.import_module('.{}'.format(modname), _package_)
    _globals_.update(**{modname: mod})

def importdir_deep(_dirname_, _package_, _globals_, filter_mod=lambda m, k, v: not k.startswith('_')):
  import os, importlib
  for f in os.listdir(_dirname_):
    if f.startswith('_') or f.startswith('.'):
      continue
    if f.endswith('.py'):
      modname = f[:-len('.py')]
    elif os.path.isdir(os.path.join(_dirname_, f)):
      modname = f
    else:
      continue
    mod = importlib.import_module('.{}'.format(modname), _package_)
    _globals_.update(**{
      k: v
      for k, v in mod.__dict__.items()
      if filter_mod(mod, k, v)
    })

def run_in_executor(f):
  import asyncio
  @functools.wraps(f)
  def inner(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return loop.run_in_executor(None, lambda: f(*args, **kwargs))
  return inner

def exception_as_dict(exc):
  if getattr(exc, 'as_dict', None) is None:
    return dict(cls=exc.__class__.__name__, message=str(exc))
  else:
    return dict(cls=exc.__class__.__name__, **exc.as_dict())
