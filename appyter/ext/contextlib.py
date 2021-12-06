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
