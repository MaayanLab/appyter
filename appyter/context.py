import os
import glob
import click
import logging
logger = logging.getLogger(__name__)
from appyter.cli import cli
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.ext.json import try_json_loads
from appyter.util import importdir_deep, join_routes

def find_fields_dir_mappings(config=None):
  assert config is not None
  cwd = config['CWD']
  profile = config['PROFILE']
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'fields') + os.path.sep] = __package__ + '.profiles.' + profile + '.fields'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'fields') + os.path.sep] = __package__ + '.profiles.default.fields'
  mappings[os.path.abspath(os.path.join(cwd, 'fields')) + os.path.sep] = 'fields'
  return mappings

def find_fields(config=None):
  assert config is not None
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

@cli.command(help='List the available fields')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
def list_fields(**kwargs):
  fields = find_fields(get_env(ipynb='app.ipynb', **kwargs))
  field_name_max_size = max(map(len, fields.keys()))
  for field, mod in fields.items():
    doc_lines = [
      *(mod.__doc__.strip().splitlines() if mod.__doc__ else []),
      *(mod.__init__.__doc__.strip().splitlines() if mod.__init__.__doc__ else []),
    ]
    doc_first_line = doc_lines[0].strip() if doc_lines else ''
    print(field.ljust(field_name_max_size+1), doc_first_line)

@cli.command(help='Describe a field using its docstring')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('field', envvar='APPYTER_FIELD', type=str)
def describe_field(field, **kwargs):
  fields = find_fields(get_env(ipynb='app.ipynb', **kwargs))
  assert field in fields, 'Please choose a valid field name, see list-fields for options'
  mod = fields[field]
  doc_lines = [
    *(mod.__doc__.strip().splitlines() if mod.__doc__ else []),
    *(mod.__init__.__doc__.strip().splitlines() if mod.__init__.__doc__ else []),
  ]
  print(*doc_lines, sep='\n')


def find_filters_dir_mappings(config=None):
  assert config is not None
  cwd = config['CWD']
  profile = config['PROFILE']
  mappings = {}
  if profile != 'default':
    mappings[os.path.join(os.path.dirname(__file__), 'profiles', profile, 'filters') + os.path.sep] = __package__ + '.profiles.' + profile + '.filters'
  mappings[os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'filters') + os.path.sep] = __package__ + '.profiles.default.filters'
  mappings[os.path.abspath(os.path.join(cwd, 'filters')) + os.path.sep] = 'filters'
  return mappings

def find_filters(config=None):
  assert config is not None
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
  assert config is not None
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
  assert config is not None
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
  assert config is not None
  return list(filter(os.path.isdir, [
    os.path.abspath(os.path.join(config['CWD'], 'templates')) + os.path.sep,
    os.path.join(os.path.dirname(__file__), 'profiles', config['PROFILE'], 'templates') + os.path.sep,
    os.path.join(os.path.dirname(__file__), 'profiles', 'default', 'templates') + os.path.sep,
  ]))

def get_extra_files(config=None):
  assert config is not None
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
  paths.add(os.path.abspath(os.path.join(config['CWD'], config['IPYNB'])))
  return list(paths)

def get_appyter_directory(path):
  return os.path.abspath(os.path.join(os.path.dirname(__file__), path))

def get_jinja2_env(context={}, config=None, session=''):
  assert config is not None
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
  env.globals.update(_config=config, _session=session, _os=os)
  env.globals.update(**build_fields(find_fields(config=config), context=context, env=env))
  return env

_mode = None
def get_env_from_kwargs(mode='default', **kwargs):
  global _mode
  if _mode is None:
    _mode = mode
  else:
    mode = _mode
  #
  import os
  import sys
  import uuid
  PREFIX = try_json_loads(kwargs.get('prefix', os.environ.get('APPYTER_PREFIX', '/')))
  PROFILE = try_json_loads(kwargs.get('profile', os.environ.get('APPYTER_PROFILE', 'default')))
  EXTRAS = try_json_loads(kwargs.get('extras', os.environ.get('APPYTER_EXTRAS', '')))
  HOST = try_json_loads(kwargs.get('host', os.environ.get('APPYTER_HOST', '127.0.0.1')))
  PORT = try_json_loads(kwargs.get('port', os.environ.get('APPYTER_PORT', 5000)))
  PROXY = try_json_loads(kwargs.get('proxy', os.environ.get('APPYTER_PROXY', False)))
  CWD = try_json_loads(os.path.abspath(kwargs.get('cwd', os.environ.get('APPYTER_CWD', str(os.getcwd())))))
  DATA_DIR = try_json_loads(kwargs.get('data_dir', os.environ.get('APPYTER_DATA_DIR', 'data')))
  DISPATCHER = try_json_loads(kwargs.get('dispatcher', os.environ.get('APPYTER_DISPATCHER')))
  DISPATCHER_URL = try_json_loads(kwargs.get('dispatcher_url', os.environ.get('APPYTER_DISPATCHER_URL')))
  DISPATCHER_IMAGE = try_json_loads(kwargs.get('dispatcher_image', os.environ.get('APPYTER_DISPATCHER_IMAGE')))
  SECRET_KEY = try_json_loads(kwargs.get('secret_key', os.environ.get('APPYTER_SECRET_KEY', str(uuid.uuid4()))))
  DEBUG = try_json_loads(kwargs.get('debug', os.environ.get('APPYTER_DEBUG', 'true')))
  STATIC_DIR = try_json_loads(kwargs.get('static_dir', os.environ.get('APPYTER_STATIC_DIR', os.path.join(CWD, 'static'))))
  STATIC_PREFIX = join_routes(PREFIX, 'static')
  IPYNB = try_json_loads(kwargs.get('ipynb', os.environ.get('APPYTER_IPYNB')))
  #
  if mode == 'default' and (IPYNB is None or not os.path.isfile(os.path.join(CWD, IPYNB))):
    logger.error('ipynb was not found')
  #
  if '://' not in DATA_DIR and not os.path.isabs(DATA_DIR):
    DATA_DIR = os.path.join(CWD, DATA_DIR)
  #
  if '://' not in STATIC_DIR and not os.path.isabs(STATIC_DIR):
    STATIC_DIR = os.path.join(CWD, STATIC_DIR)
  #
  if os.path.abspath(CWD) not in sys.path:
    sys.path.insert(0, CWD)
  if CWD not in os.environ['PATH'].split(':'):
    os.environ['PATH'] = CWD + ':' + os.environ['PATH']
  #
  return dict(
    MODE=mode,
    PREFIX=PREFIX,
    PROFILE=PROFILE,
    EXTRAS=EXTRAS,
    HOST=HOST,
    PORT=PORT,
    PROXY=PROXY,
    CWD=CWD,
    DATA_DIR=DATA_DIR,
    DISPATCHER=DISPATCHER,
    DISPATCHER_URL=DISPATCHER_URL,
    DISPATCHER_IMAGE=DISPATCHER_IMAGE,
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
  except RuntimeError:
    pass
  except AssertionError:
    pass
  #
  return config
