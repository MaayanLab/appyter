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
