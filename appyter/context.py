import os
import glob
from appyter.util import importdir_deep

def find_fields_dir_mappings(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'fields') + os.path.sep] = __package__ + '.profiles.' + profile + '.fields'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'fields') + os.path.sep] = __package__ + '.profiles.default.fields'
  mappings[os.path.abspath(os.path.join(cwd, 'fields')) + os.path.sep] = 'fields'
  return mappings

def find_fields(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  from appyter.fields import Field
  ctx = {}
  for _dirname_, _package_ in find_fields_dir_mappings(config=config).items():
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=lambda m, k, v: not k.startswith('_') and isinstance(v, type) and issubclass(v, Field)
      )
  return ctx

def find_filters_dir_mappings(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'filters') + os.path.sep] = __package__ + '.profiles.' + profile + '.filters'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'filters') + os.path.sep] = __package__ + '.profiles.default.filters'
  mappings[os.path.abspath(os.path.join(cwd, 'filters')) + os.path.sep] = 'filters'
  return mappings

def find_filters(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  ctx = {}
  for _dirname_, _package_ in find_filters_dir_mappings(config=config).items():
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=lambda m, k, v: not k.startswith('_') and isinstance(v, type(lambda: None))
      )
  return ctx

def find_blueprints_dir_mappings(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
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

def find_blueprints(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  ctx = {}
  for _dirname_, _package_ in find_blueprints_dir_mappings(config=config).items():
    if os.path.isdir(_dirname_):
      importdir_deep(
        _dirname_,
        _package_,
        ctx,
        filter_mod=filter_blueprints,
      )
  return ctx

def find_templates_dir(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  return list(filter(os.path.isdir, [
    os.path.abspath(os.path.join(cwd, 'templates')) + os.path.sep,
    os.path.join(os.path.dirname(__file__), 'profiles', profile, 'templates') + os.path.sep,
    os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'templates') + os.path.sep,
  ]))

def get_extra_files(config=None):
  if config is None:
    config = get_env()
  cwd = config['CWD']
  profile = config['PROFILE']
  dirs = [
    *find_templates_dir(config=config),
    *find_filters_dir_mappings(config=config).keys(),
    *find_fields_dir_mappings(config=config).keys(),
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
  paths.add(os.path.abspath(os.path.join(cwd, config['IPYNB'])))
  return list(paths)

def get_jinja2_env(context={}, config=None):
  if config is None:
    config = get_env()
  #
  import sys
  from appyter.fields import build_fields
  from jinja2 import Environment, ChoiceLoader, FileSystemLoader
  env = Environment(
    extensions=['jinja2.ext.do'],
    loader=ChoiceLoader([
      FileSystemLoader(d)
      for d in find_templates_dir(config=config)
    ]),
  )
  env.filters.update(**find_filters(config=config))
  env.globals.update(**find_filters(config=config))
  env.globals.update(_config=config)
  env.globals.update(**build_fields(find_fields(config=config), context=context))
  return env

def try_json_loads(v):
  import json
  try:
    return json.loads(v)
  except:
    return v

def get_env_from_kwargs(**kwargs):
  import sys
  import uuid
  from appyter.util import join_routes
  assert kwargs != {}
  PREFIX = kwargs.get('prefix', os.environ.get('PREFIX', '/'))
  PROFILE = kwargs.get('profile', os.environ.get('PROFILE', 'default'))
  HOST = kwargs.get('host', os.environ.get('HOST', '127.0.0.1'))
  PORT = try_json_loads(kwargs.get('port', os.environ.get('PORT', 5000)))
  PROXY = try_json_loads(kwargs.get('proxy', os.environ.get('PROXY', False)))
  CWD = os.path.realpath(kwargs.get('cwd', os.environ.get('CWD', os.getcwd())))
  DATA_DIR = kwargs.get('data-dir', os.environ.get('DATA_DIR', 'data'))
  MAX_THREADS = try_json_loads(kwargs.get('max-threads', os.environ.get('MAX_THREADS', 10)))
  SECRET_KEY = kwargs.get('secret-key', os.environ.get('SECRET_KEY', str(uuid.uuid4())))
  DEBUG = try_json_loads(kwargs.get('debug', os.environ.get('DEBUG', 'true')))
  STATIC_DIR = kwargs.get('static-dir', os.path.abspath(os.path.join(CWD, 'static')))
  STATIC_PREFIX = join_routes(PREFIX, 'static')
  IPYNB = kwargs.get('ipynb', os.environ.get('IPYNB'))
  assert IPYNB != None, 'ipynb was not found'
  #
  if os.path.abspath(CWD) not in sys.path:
    sys.path.insert(0, os.path.abspath(CWD))
  if os.path.abspath(CWD) not in os.environ['PATH'].split(':'):
    os.environ['PATH'] = os.path.abspath(CWD) + ':' + os.environ['PATH']
  #
  return dict(
    PREFIX=PREFIX,
    PROFILE=PROFILE,
    HOST=HOST,
    PORT=PORT,
    PROXY=PROXY,
    CWD=CWD,
    DATA_DIR=DATA_DIR,
    MAX_THREADS=MAX_THREADS,
    SECRET_KEY=SECRET_KEY,
    DEBUG=DEBUG,
    STATIC_DIR=STATIC_DIR,
    IPYNB=IPYNB,
    STATIC_PREFIX=STATIC_PREFIX,
  )

def get_env_from_click():
  ''' Traverse click context and use params for get_env_from_kwargs
  '''
  import click
  click_ctx = click.get_current_context()
  # aggregate all params from all parents
  params = {}
  while click_ctx:
    # preserve leaf-values in the case of conflicts
    params = {
      k: params.get(k, click_ctx.params.get(k))
      for k in (click_ctx.params.keys() | params.keys())
    }
    click_ctx = click_ctx.parent
  # use aggregated params to get env
  return get_env_from_kwargs(**params)

def get_env_from_flask():
  ''' If we're running in flask, current_app.config should be available
  '''
  from flask import current_app
  return current_app.config

config = {}

def get_env(**kwargs):
  ''' Try various methods to grab the application config
  (different based on whether we're in a flask thread/somewhere else)
  '''
  #
  try:
    global config
    config = get_env_from_kwargs(**kwargs)
  except AssertionError:
    pass
  #
  try:
    return get_env_from_flask()
  except Exception:
    pass
  #
  try:
    return get_env_from_click()
  except RuntimeError as e:
    pass
  except AssertionError as e:
    pass
  #
  return config
