async def alist(agen):
  ''' Resolve all values from an asynchronous generator like it was an iterator
  '''
  L = []
  async for el in agen:
    L.append(el)
  return L

def ensure_list(L):
  if type(L) == list:
    return L
  else:
    return [L]

def collapse(L):
  if len(L) == 1:
    return L[0]
  else:
    return L

def one_and_only(it):
  it = iter(it)
  try:
    ret = next(it)
    try:
      next(it)
      raise Exception('Expected one got multiple')
    except StopIteration:
      pass
  except StopIteration:
    raise Exception('Expected one got none')
  return ret
