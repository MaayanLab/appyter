import json

def pyeval(v, **kwargs):
  ''' DO NOT USE THIS WITH USER INPUT,
  It helps with running python code like list comprehensions in jinja.
  '''
  return eval(v, kwargs)
