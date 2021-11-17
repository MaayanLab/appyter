def importdir(_dirname_, _package_, _globals_):
  import pathlib, importlib
  _dirname_ = pathlib.Path(_dirname_)
  for f in _dirname_.glob('[!_.]*'):
    if f.is_file() and f.suffix == '.py':
      modname = f.stem
    elif f.is_dir():
      modname = f.name
    else:
      continue
    mod = importlib.import_module('.{}'.format(modname), _package_)
    _globals_.update(**{modname: mod})

def importdir_deep(_dirname_, _package_, _globals_, filter_mod=lambda m, k, v: not k.startswith('_')):
  import pathlib, importlib
  _dirname_ = pathlib.Path(_dirname_)
  for f in _dirname_.glob('[!_.]*'):
    if f.is_file() and f.suffix == '.py':
      modname = f.stem
    elif f.is_dir():
      modname = f.name
    else:
      continue
    mod = importlib.import_module('.{}'.format(modname), _package_)
    _globals_.update(**{
      k: v
      for k, v in mod.__dict__.items()
      if filter_mod(mod, k, v)
    })
