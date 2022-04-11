def dict_filter_none(d):
  return { k: v for k, v in d.items() if v }

def dict_collision_free_update(d, **kwargs):
  for k, v in kwargs.items():
    assert k not in d, 'Collision in update'
    d[k] = v

def dict_flatten(d):
  Q = [(tuple(), d)]
  F = []
  while Q:
    K, V = Q.pop()
    if type(V) == dict:
      for k, v in V.items():
        Q.append(((*K, k), v))
    else:
      F.append((K, V))
  return F

def dict_unflatten(f):
  D = {}
  for K, v in f:
    o = D
    for k in K[:-1]:
      if k not in o:
        o[k] = {}
      o = o[k]
    o[K[-1]] = v
  return D

def dict_merge(d, **kwargs):
  return dict_unflatten(dict_flatten(d) + dict_flatten(kwargs))

def expand_dotmap(dotmap):
  ''' Convert dot-notation into deep dict
  '''
  params = {}
  for K, v in dotmap.items():
    _params_n_2 = None
    _params_n_1 = params
    for k in K.split('.'):
      if k not in _params_n_1: _params_n_1[k] = {}
      _params_n_2 = _params_n_1
      _params_n_1 = _params_n_2[k]
    _params_n_2[k] = v
  return params
