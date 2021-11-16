
def dict_filter_none(d):
  return { k: v for k, v in d.items() if v }

def dict_flatten(d):
  Q = [(tuple(), d)]
  F = set()
  while Q:
    K, V = Q.pop()
    if type(V) == dict:
      for k, v in V.items():
        Q.append(((*K, k), v))
    else:
      F.add((K, V))
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
  return dict_unflatten(dict_flatten(d) | dict_flatten(kwargs))
