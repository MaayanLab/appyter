import click
from appyter.ext.json import try_json_loads, try_json_dumps

class Json(click.ParamType):
  name = 'Json'

  def convert(self, value, param, ctx):
    return try_json_loads(value)

  def split_envvar_value(self, rv):
    v = try_json_loads(rv)
    return v if type(v) == list else [v]

def click_option_setenv(spec, envvar=None, **kwargs):
  ''' Like click.option but explicitly set os.environ as well.
  '''
  import os, re, functools
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
  import os, re, functools
  def decorator(func):
    @click.argument(var, envvar=envvar, **kwargs)
    @functools.wraps(func)
    def wrapper(**kwargs):
      os.environ[envvar] = try_json_dumps(kwargs[var.replace('-', '_')])
      return func(**kwargs)
    return wrapper
  return decorator
