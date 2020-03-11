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

def find_fields():
  from jupyter_template.fields import Field
  ctx = {}
  dirs = [
    (os.path.join(os.path.dirname(__file__), 'default', 'fields'), __package__ + '.default.fields'),
    (os.path.join(os.getcwd(), 'fields'), 'fields'),
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

def find_filters():
  ctx = {}
  dirs = [
    (os.path.join(os.path.dirname(__file__), 'default', 'filters'), __package__ + '.default.filters'),
    (os.path.join(os.getcwd(), 'filters'), 'filters'),
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

def find_template_dirs():
  return list(filter(os.path.isdir, [
    os.path.join(os.path.dirname(__file__), 'default', 'templates'),
    os.path.join(os.getcwd(), 'templates'),
  ]))

def get_jinja2_env(context={}):
  from jupyter_template.fields import build_fields
  from jinja2 import Environment, ChoiceLoader, FileSystemLoader
  env = Environment(
    extensions=['jinja2.ext.do'],
    loader=ChoiceLoader([
      FileSystemLoader(d)
      for d in find_template_dirs()
    ]),
  )
  env.filters.update(**find_filters())
  env.globals.update(**build_fields(find_fields(), context=context))
  return env
