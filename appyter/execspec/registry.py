# inspired by from https://github.com/fsspec/filesystem_spec

_registry = {}
def register_implementation(name, cls):
  global _registry
  _registry[name] = cls

known_implementations = {
  'dispatch': {'class': 'appyter.execspec.implementations.dispatch.DispatchExecutor'},
  'docker': {'class': 'appyter.execspec.implementations.docker.DockerExecutor'},
  'kube': {'class': 'appyter.execspec.implementations.kube.KubernetesExecutor'},
  'local': {'class': 'appyter.execspec.implementations.local.LocalExecutor'},
  'subprocess': {'class': 'appyter.execspec.implementations.subprocess.SubprocessExecutor'},
  'wes': {'class': 'appyter.execspec.implementations.wes.WESExecutor'},
  'cavatica': {'class': 'appyter.execspec.implementations.cavatica.CavaticaExecutor'},
}

def get_executor_class(protocol):
  global _registry
  if protocol not in _registry:
    if protocol not in known_implementations:
      raise ValueError(f"Protocol not known: {protocol}")
    bit = known_implementations[protocol]
    try:
      register_implementation(protocol, _import_class(bit['class']))
    except ImportError as e:
      raise ImportError(bit['err']) from e
  cls = _registry[protocol]
  return cls

def _import_class(cls, minv=None):
    """Take a string FQP and return the imported class or identifier
    clas is of the form "package.module.klass" or "package.module:subobject.klass"
    """
    import importlib
    if ":" in cls:
      mod, name = cls.rsplit(":", 1)
      mod = importlib.import_module(mod)
      for part in name.split("."):
        mod = getattr(mod, part)
      return mod
    else:
      mod, name = cls.rsplit(".", 1)
      mod = importlib.import_module(mod)
      return getattr(mod, name)

def executor(protocol, **executor_options):
  cls = get_executor_class(protocol)
  return cls(**executor_options)
