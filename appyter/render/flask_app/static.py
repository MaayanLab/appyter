''' Represent the areas that can be handled externally in production
'''
import os
from flask import request, current_app, send_file, send_from_directory, abort

from appyter.render.flask_app.core import core
from appyter.render.flask_app.util import route_join_with_or_without_slash
from appyter.context import get_profile_directory


@route_join_with_or_without_slash(core, methods=['GET'])
def get_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
    'application/json',
  ], 'text/html')
  if mimetype in {'text/html'}:
    return send_file(os.path.join(current_app.config['CWD'], current_app.config['DATA_DIR'], 'index.html'))
  elif mimetype in {'application/json'}:
    return send_file(os.path.join(current_app.config['CWD'], current_app.config['DATA_DIR'], 'index.json'))
  elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
    return send_file(current_app.config['IPYNB'])
  else:
    abort(404)

@route_join_with_or_without_slash(core, 'favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(current_app.config['STATIC_DIR'], 'favicon.ico')

@route_join_with_or_without_slash(core, 'static', '<path:path>', methods=['GET'])
def static_files(path):
  return send_from_directory(current_app.config['STATIC_DIR'], path)

@route_join_with_or_without_slash(core, 'profile', '<path:path>', methods=['GET'])
def profile(path):
  return send_from_directory(os.path.join(get_profile_directory('default'), 'static'), path)

@route_join_with_or_without_slash(core, '<path:path>', methods=['GET'])
def data_files(path):
  if path.endswith('/'):
    path = '/'.join((path[:-1], 'index.html'))
  return send_from_directory(os.path.join(current_app.config['DATA_DIR'], 'output'), path)
