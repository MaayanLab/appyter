''' Represent the areas that can be handled externally in production
'''
import os
from flask import request, current_app, send_file, send_from_directory, abort

from appyter.ext.fs import Filesystem
from appyter.render.flask_app.core import core
from appyter.render.flask_app.util import route_join_with_or_without_slash
from appyter.context import get_profile_directory


@route_join_with_or_without_slash(core, methods=['GET'])
def get_index():
  fs = Filesystem(current_app.config['CWD'])
  data_fs = Filesystem(current_app.config['DATA_DIR'])
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
    'application/json',
  ], 'text/html')
  if mimetype in {'text/html'}:
    return send_file(data_fs.open('index.html', 'r'), mimetype=mimetype)
  elif mimetype in {'application/json'}:
    return send_file(data_fs.open('index.json', 'r'), mimetype=mimetype)
  elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
    return send_file(fs.open(current_app.config['IPYNB'], 'r'), mimetype=mimetype)
  else:
    abort(404)

@route_join_with_or_without_slash(core, 'favicon.ico', methods=['GET'])
def favicon():
  # TODO: use Filesystem
  return send_from_directory(current_app.config['STATIC_DIR'], 'favicon.ico')

@route_join_with_or_without_slash(core, 'static', '<path:path>', methods=['GET'])
def static_files(path):
  # TODO: use Filesystem
  return send_from_directory(current_app.config['STATIC_DIR'], path)

@route_join_with_or_without_slash(core, 'profile', '<path:path>', methods=['GET'])
def profile(path):
  # TODO: use Filesystem
  return send_from_directory(os.path.join(get_profile_directory('default'), 'static'), path)

@route_join_with_or_without_slash(core, '<path:path>', methods=['GET'])
def data_files(path):
  # TODO: use Filesystem
  if path.endswith('/'):
    path = '/'.join((path[:-1], 'index.html'))
  return send_from_directory(os.path.join(current_app.config['DATA_DIR'], 'output'), path)
