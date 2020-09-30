import os

def url_for(directory, **kwargs):
  from appyter.context import get_env
  config = get_env()
  if config['DEBUG']:
    try:
      from flask import url_for
      if directory == 'static':
        directory = '.'.join(('__main__', directory))
      return url_for(directory, **kwargs)
    except RuntimeError:
      filename = kwargs.get('filename', kwargs.get('path'))
      assert filename is not None
      return os.path.join(directory, filename)
  else:
    filename = kwargs.get('filename', kwargs.get('path'))
    assert filename is not None
    return os.path.join(config['PREFIX'], directory, filename)
