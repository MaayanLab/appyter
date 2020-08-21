import os

def url_for(directory, **kwargs):
  try:
    from flask import url_for
    if directory == 'static':
      directory = '__main__.static'
    return url_for(directory, **kwargs)
  except RuntimeError:
    filename = kwargs['filename']
    return os.path.join(directory, filename)
