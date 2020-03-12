import os, os.path
import importlib

def importdir(_dirname_, _package_, _globals_):
  for f in os.listdir(_dirname_):
    if f.startswith('_'):
      continue
    if f.endswith('.py'):
      modname = f[:-len('.py')]
    elif os.path.isdir(os.path.join(_dirname_, f)):
      modname = f
    else:
      continue
    mod = importlib.import_module('.{}'.format(modname), _package_)
    _globals_.update(**{modname: mod})

def importdir_deep(_dirname_, _package_, _globals_, filter_mod=lambda k, v: not k.startswith('_')):
  for f in os.listdir(_dirname_):
    if f.startswith('_'):
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
      if filter_mod(k, v)
    })

def find_fields(cwd=os.getcwd(), profile='default'):
  from jupyter_template.fields import Field
  ctx = {}
  dirs = [
    (os.path.join(os.path.dirname(__file__), 'profiles', profile, 'fields'), __package__ + '.profiles.' + profile + '.fields'),
    (os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'fields'), __package__ + '.profiles.default.fields'),
    (os.path.join(cwd, 'fields'), 'fields'),
  ]
  for _dirname_, _package_ in dirs:
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=lambda k, v: not k.startswith('_') and isinstance(v, type) and issubclass(v, Field)
      )
  return ctx

def find_filters(cwd=os.getcwd(), profile='default'):
  ctx = {}
  dirs = [
    (os.path.join(os.path.dirname(__file__), 'profiles', profile, 'filters'), __package__ + '.profiles.' + profile + '.filters'),
    (os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'filters'), __package__ + '.profiles.default.filters'),
    (os.path.join(cwd, 'filters'), 'filters'),
  ]
  for _dirname_, _package_ in dirs:
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=lambda k, v: not k.startswith('_') and isinstance(v, type(lambda: None))
      )
  return ctx

def find_template_dirs(cwd=os.getcwd(), profile='default'):
  return list(filter(os.path.isdir, [
    os.path.join(os.path.dirname(__file__), 'profiles', profile, 'templates'),
    os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'templates'),
    os.path.join(cwd, 'templates'),
  ]))

def get_jinja2_env(context={}, cwd=None, profile=None):
  _, _, kwargs = get_sys_env()
  cwd = kwargs.get('cwd', os.getcwd())
  profile = kwargs.get('profile', 'default')

  import sys
  from jupyter_template.fields import build_fields
  from jinja2 import Environment, ChoiceLoader, FileSystemLoader
  sys.path.insert(0, cwd)
  env = Environment(
    extensions=['jinja2.ext.do'],
    loader=ChoiceLoader([
      FileSystemLoader(d)
      for d in find_template_dirs(cwd=cwd, profile=profile)
    ]),
  )
  env.filters.update(**find_filters(cwd=cwd, profile=profile))
  env.globals.update(**build_fields(find_fields(cwd=cwd, profile=profile), context=context))
  return env

def get_sys_env():
  import sys
  from collections import Counter
  args = []
  kargs = Counter()
  kwargs = {}
  for arg in sys.argv[1:]:
    if arg.startswith('--'):
      try:
        k, v = arg[2:].split('=', maxsplit=1)
      except:
        k, v = arg[2:], True
      kwargs[k] = v
    elif arg.startswith('-'):
      kargs.update({arg[1:]: 1})
    else:
      args.append(arg)
  return args, kargs, kwargs
