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
    return send_file(data_fs.open('index.html', 'rb'), attachment_filename='index.html', mimetype=mimetype)
  elif mimetype in {'application/json'}:
    return send_file(data_fs.open('index.json', 'rb'), attachment_filename='index.json', mimetype=mimetype)
  elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
    return send_file(fs.open(current_app.config['IPYNB'], 'rb'), attachment_filename=current_app.config['IPYNB'], mimetype=mimetype)
  else:
    abort(404)

@core.route('/favicon.ico', methods=['GET'])
def favicon():
  satic_fs = Filesystem(current_app.config['STATIC_DIR'])
  if satic_fs.exists('favicon.ico'):
    return send_file(satic_fs.open('favicon.ico', 'rb'), attachment_filename='favicon.ico')
  abort(404)

@core.route('/static/<path:filename>', methods=['GET'])
def static(filename):
  satic_fs = Filesystem(current_app.config['STATIC_DIR'])
  if satic_fs.exists(filename):
    return send_file(satic_fs.open(filename, 'rb'), attachment_filename=filename)
  abort(404)

@core.route('/profile/<path:path>', methods=['GET'])
def profile(path):
  return send_from_directory(os.path.join(get_profile_directory('default'), 'static'), path)

@route_join_with_or_without_slash(core, '<path:path>', methods=['GET'])
def data_files(path):
  data_fs = Filesystem(Filesystem.join(current_app.config['DATA_DIR'], 'output'))
  if path.endswith('/'):
    path = '/'.join((path[:-1], 'index.html'))
  if data_fs.exists(path):
    return send_file(data_fs.open(path, 'rb'), attachment_filename=os.path.basename(path))
  abort(404)
