def dict_filter_none(d):
  return { k: v for k, v in d.items() if v is not None }

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

def dict_typed_flatten(d):
  ''' dict_flatten but preserves lists & ordering
  '''
  Q = [(tuple(), d)]
  F = []
  while Q:
    K, V = Q.pop()
    if type(V) == dict:
      for k, v in V.items():
        Q.append(((*K, dict, k), v))
    elif type(V) == list:
      for k, v in enumerate(V):
        Q.append(((*K, list, k), v))
    else:
      F.append((K, V))
  return F

def dict_typed_unflatten(f):
  ''' opposite of dict_typed_unflatten
  '''
  D = {}
  for K, v in f:
    o = D
    for k, typ in zip(K[1:-1:2], K[2:-1:2]):
      if type(o) == dict and k not in o:
        o[k] = typ()
      elif type(o) == list and len(o) < k or o[k] is None:
        while len(o) <= k: o.append(None)
        o[k] = typ()
      #
      if type(o) == list:
        while len(o) <= k: o.append(None)
      o = o[k]
    if type(o) == list:
      while len(o) <= K[-1]: o.append(None)
    o[K[-1]] = v
  return D
