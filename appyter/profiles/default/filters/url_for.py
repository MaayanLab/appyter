def url_for(directory, public=False, **kwargs):
  from appyter.context import get_env
  from appyter.ext.urllib import join_url
  config = get_env()
  url = None
  if config['DEBUG']:
    # appyter debugging static serve mode in flask
    try:
      from flask import url_for as _url_for
      modified_directory = '.'.join(('__main__', directory)) if directory == 'static' else directory
      url = _url_for(modified_directory, **kwargs).rstrip('/')
    except RuntimeError:
      pass
  #
  if url is None:
    # url_for outside of flask
    filename = kwargs.get('filename', kwargs.get('path'))
    assert filename is not None
    url = join_url(config['PREFIX'], directory, filename)
  #
  if config['MODE'] == 'default' and public:
    # url_for public modifier -- return the public facing url
    try:
      from flask import request
      url = join_url(request.url_root, url)
    except RuntimeError:
      raise
    except:
      pass
  #
  if config['MODE'] == 'magic':
    # jupyter notebook magic mode
    if url.startswith('/'):
      url = url[1:]
  #
  return url
