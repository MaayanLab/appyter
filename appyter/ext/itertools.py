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
