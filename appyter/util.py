import json
import urllib.parse
from werkzeug.utils import secure_filename

def try_json_loads(v):
  try:
    return json.loads(v)
  except:
    return v

def try_json_dumps(v):
  if type(v) == str:
    return v
  else:
    return json.dumps(v)

def dict_filter_none(d):
  return { k: v for k, v in d.items() if v }

def join_routes(*routes):
  ''' Utility function for joining routes while striping extraneous slashes
  '''
  return '/' + '/'.join([route.strip('/') for route in routes if route.strip('/')])

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

def click_option_setenv(spec, envvar=None, **kwargs):
  ''' Like click.option but explicitly set os.environ as well.
  '''
  import os, re, functools, click
  m = re.match(r'^--(.+)$', spec)
  assert m
  var = m.group(1).replace('-', '_')
  def decorator(func):
    @click.option(spec, envvar=envvar, **kwargs)
    @functools.wraps(func)
    def wrapper(**kwargs):
      if kwargs.get(var) is not None:
        os.environ[envvar] = try_json_dumps(kwargs[var])
      return func(**kwargs)
    return wrapper
  return decorator

def click_argument_setenv(var, envvar=None, **kwargs):
  ''' Like click.argument but explicitly set os.environ as well.
  '''
  import os, re, functools, click
  def decorator(func):
    @click.argument(var, envvar=envvar, **kwargs)
    @functools.wraps(func)
    def wrapper(**kwargs):
      os.environ[envvar] = try_json_dumps(kwargs[var.replace('-', '_')])
      return func(**kwargs)
    return wrapper
  return decorator
