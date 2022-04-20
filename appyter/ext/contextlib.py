import sys
import contextlib

@contextlib.contextmanager
def with_many(**withables):
  ctx = {
    name: withable.__enter__()
    for name, withable in withables.items()
  }
  try:
    yield ctx
  except:
    for withable in withables.values():
      withable.__exit__(*sys.exc_info())
  else:
    for withable in withables.values():
      withable.__exit__(None, None, None)

@contextlib.contextmanager
def ensure_context(obj):
  if getattr(obj, '__enter__', None) is not None:
    ctx = obj.__enter__()
  else:
    ctx = obj
  try:
    yield ctx
  except:
    if getattr(obj, '__exit__', None) is not None:
      obj.__exit__(*sys.exc_info())
    else:
      raise
  else:
    if getattr(obj, '__exit__', None) is not None:
      obj.__exit__(None, None, None)

class ContextManagerAsHandle:
  def __init__(self, inner):
    self.inner = inner
  
  def open(self):
    return self.inner.__enter__()
  
  def close(self):
    return self.inner.__exit__(None, None, None)
