import os

def url_for(directory, production=None, **kwargs):
  if production is not None:
    filename = kwargs.get('filename', kwargs.get('path'))
    assert filename is not None
    return os.path.join(production['PREFIX'], directory, filename)
  try:
    from flask import url_for
    if directory == 'static' or directory == 'profile':
      directory = '.'.join(('__main__', directory))
    return url_for(directory, **kwargs)
  except RuntimeError:
    filename = kwargs.get('filename', kwargs.get('path'))
    assert filename is not None
    return os.path.join(directory, filename)
