import os

def url_for(directory, **kwargs):
  from appyter.context import get_env
  config = get_env()
  if config['DEBUG']:
    try:
      from flask import url_for
      modified_directory = '.'.join(('__main__', directory)) if directory == 'static' else directory
      return url_for(modified_directory, **kwargs)
    except RuntimeError:
      filename = kwargs.get('filename', kwargs.get('path'))
      assert filename is not None
      return os.path.join(directory, filename)
  else:
    filename = kwargs.get('filename', kwargs.get('path'))
    assert filename is not None
    return os.path.join(config['PREFIX'], directory, filename)
