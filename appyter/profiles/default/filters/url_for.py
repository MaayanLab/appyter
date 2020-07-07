import os

def url_for(directory, filename=None):
  assert type(filename) == str, 'Filename should be a string and is not optional'
  try:
    from flask import url_for
    return url_for(directory, filename=filename)
  except RuntimeError:
    return os.path.join(directory, filename)
