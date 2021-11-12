def ensure_callable(var):
  if callable(var):
    return var
  else:
    return lambda: var

_memcache = {}
def memcached(func):
  ''' Cache all calls to this function in memory permanently
  '''
  global _memcache
  if func not in _memcache:
    _memcache[func] = {}
  from functools import wraps
  @wraps(func)
  def wrapper(*args, **kwargs):
    _h = hash((args, frozenset(kwargs.items())))
    if _h not in _memcache[func]:
      _memcache[func][_h] = func(*args, **kwargs)
    return _memcache[func][_h]
  return wrapper
