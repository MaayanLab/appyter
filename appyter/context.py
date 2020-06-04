import glob
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

def importdir_deep(_dirname_, _package_, _globals_, filter_mod=lambda m, k, v: not k.startswith('_')):
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
      if filter_mod(mod, k, v)
    })

def find_fields_dir_mappings(cwd=os.getcwd(), profile='default'):
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'fields') + os.path.sep] = __package__ + '.profiles.' + profile + '.fields'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'fields') + os.path.sep] = __package__ + '.profiles.default.fields'
  mappings[os.path.abspath(os.path.join(cwd, 'fields')) + os.path.sep] = 'fields'
  return mappings

def find_fields(cwd=os.getcwd(), profile='default'):
  from appyter.fields import Field
  ctx = {}
  for _dirname_, _package_ in find_fields_dir_mappings(cwd=cwd, profile=profile).items():
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=lambda m, k, v: not k.startswith('_') and isinstance(v, type) and issubclass(v, Field)
      )
  return ctx

def find_filters_dir_mappings(cwd=os.getcwd(), profile='default'):
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'filters') + os.path.sep] = __package__ + '.profiles.' + profile + '.filters'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'filters') + os.path.sep] = __package__ + '.profiles.default.filters'
  mappings[os.path.abspath(os.path.join(cwd, 'filters')) + os.path.sep] = 'filters'
  return mappings

def find_filters(cwd=os.getcwd(), profile='default'):
  ctx = {}
  for _dirname_, _package_ in find_filters_dir_mappings(cwd=cwd, profile=profile).items():
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=lambda m, k, v: not k.startswith('_') and isinstance(v, type(lambda: None))
      )
  return ctx

def find_blueprints_dir_mappings(cwd=os.getcwd(), profile='default'):
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'blueprints') + os.path.sep] = __package__ + '.profiles.' + profile + '.blueprints'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'blueprints') + os.path.sep] = __package__ + '.profiles.default.blueprints'
  mappings[os.path.abspath(os.path.join(cwd, 'blueprints')) + os.path.sep] = 'blueprints'
  return mappings

def filter_blueprints(m, k, v):
  from flask import Blueprint
  if isinstance(v, Blueprint):
    return True
  elif callable(v):
    if m.__name__.startswith('blueprints') and 'blueprints.' + k == m.__name__:
      return True
  return False

def find_blueprints(cwd=os.getcwd(), profile='default'):
  ctx = {}
  for _dirname_, _package_ in find_blueprints_dir_mappings(cwd=cwd, profile=profile).items():
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=filter_blueprints,
      )
  return ctx

def find_templates_dir(cwd=os.getcwd(), profile='default'):
  return list(filter(os.path.isdir, [
    os.path.abspath(os.path.join(cwd, 'templates')) + os.path.sep,
    os.path.join(os.path.dirname(__file__), 'profiles', profile, 'templates') + os.path.sep,
    os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'templates') + os.path.sep,
  ]))

def get_extra_files(cwd=None, profile=None):
  args, _, kwargs = get_sys_env()
  cwd = kwargs.get('cwd', os.getcwd())
  profile = kwargs.get('profile', 'default')
  dirs = [
    *find_templates_dir(cwd=cwd, profile=profile),
    *find_filters_dir_mappings(cwd=cwd, profile=profile).keys(),
    *find_fields_dir_mappings(cwd=cwd, profile=profile).keys(),
  ]
  paths = {
    os.path.abspath(f) + (os.path.sep if os.path.isdir(f) else '')
    for d in dirs
    for f in ({
      d,
      # all files recursively in these directories
      *glob.glob(os.path.join(d, '**'), recursive=True),
    } - ({
      # exclude directories or files that begin with _
      *glob.glob(os.path.join(d, '_**', '*'), recursive=True),
      *glob.glob(os.path.join(d, '**', '_*'), recursive=True),
    }))
  }
  paths.add(os.path.abspath(args[0]))
  return list(paths)

def get_jinja2_env(context={}, cwd=None, profile=None, prefix=None, debug=True):
  args, kargs, kwargs = get_sys_env()
  if cwd is None:
    cwd = kwargs.get('cwd', os.getcwd())
  if profile is None:
    profile = kwargs.get('profile', 'default')
  if prefix is None:
    prefix = kwargs.get('prefix', '/')

  import sys
  from appyter.fields import build_fields
  from jinja2 import Environment, ChoiceLoader, FileSystemLoader
  if os.path.abspath(cwd) not in sys.path:
    sys.path.insert(0, os.path.abspath(cwd))
  if os.path.abspath(cwd) not in os.environ['PATH'].split(':'):
    os.environ['PATH'] = os.path.abspath(cwd) + ':' + os.environ['PATH']
  env = Environment(
    extensions=['jinja2.ext.do'],
    loader=ChoiceLoader([
      FileSystemLoader(d)
      for d in find_templates_dir(cwd=cwd, profile=profile)
    ]),
  )
  env.filters.update(**find_filters(cwd=cwd, profile=profile))
  env.globals.update(**find_filters(cwd=cwd, profile=profile))
  env.globals.update(
    _prefix=prefix,
    _debug=debug,
    _args=args,
    _kargs=kargs,
    _kwargs=kwargs,
  )
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
