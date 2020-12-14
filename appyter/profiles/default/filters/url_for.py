import os

def url_for(directory, public=False, **kwargs):
  from appyter.context import get_env
  from appyter.util import safe_join, join_routes
  config = get_env()
  url = None
  if config['DEBUG']:
    try:
      from flask import url_for
      modified_directory = '.'.join(('__main__', directory)) if directory == 'static' else directory
      url = url_for(modified_directory, **kwargs)
    except:
      pass
  #
  if url is None:
    filename = kwargs.get('filename', kwargs.get('path'))
    assert filename is not None
    url = safe_join(config['PREFIX'], directory, filename)
  #
  if public:
    try:
      from flask import request
      url = join_routes(request.url_root, url)[1:]
    except:
      pass
  #
  return url
