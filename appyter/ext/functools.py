def ensure_callable(var):
  if callable(var):
    return var
  else:
    return lambda: var
