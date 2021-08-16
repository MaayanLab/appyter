''' Represent the areas that can be handled externally in production
'''
import os
from flask import request, current_app, send_file, send_from_directory, abort, jsonify
from werkzeug.exceptions import NotFound

from appyter.ext.fs import Filesystem
from appyter.render.flask_app.core import core
from appyter.render.flask_app.util import route_join_with_or_without_slash
from appyter.context import get_appyter_directory
from appyter.parse.nb import nb_from_ipynb_io
from appyter.render.form import render_form_from_nbtemplate
from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
from appyter.context import get_jinja2_env


@route_join_with_or_without_slash(core, methods=['GET'])
def get_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/json',
    'application/vnd.jupyter',
  ], 'text/html')
  fs = Filesystem(current_app.config['CWD'])
  if mimetype in {'text/html'}:
    with fs.open(current_app.config['IPYNB'], 'r') as fr:
      env = get_jinja2_env(config=current_app.config)
      nbtemplate = nb_from_ipynb_io(fr)
    return render_form_from_nbtemplate(env, nbtemplate)
  elif mimetype in {'application/json'}:
    with fs.open(current_app.config['IPYNB'], 'r') as fr:
      env = get_jinja2_env(config=current_app.config)
      nbtemplate = nb_from_ipynb_io(fr)
    return jsonify(render_nbtemplate_json_from_nbtemplate(env, nbtemplate))
  elif mimetype in {'application/vnd.jupyter'}:
    return send_file(fs.open(current_app.config['IPYNB'], 'rb'), attachment_filename=current_app.config['IPYNB'], mimetype=mimetype)
  else:
    abort(404)

@core.route('/favicon.ico', methods=['GET'])
def favicon():
  static = Filesystem(current_app.config['STATIC_DIR'])
  if static.exists('favicon.ico'):
    return send_file(static.open('favicon.ico', 'rb'), attachment_filename='favicon.ico')
  abort(404)

@core.route('/static/<path:filename>', methods=['GET'])
def static(filename):
  static = Filesystem(current_app.config['STATIC_DIR'])
  if static.exists(filename):
    return send_file(static.open(filename, 'rb'), attachment_filename=filename)
  #
  try:
    return send_from_directory(get_appyter_directory(f"profiles/{current_app.config['PROFILE']}/static"), path=filename)
  except NotFound:
    return send_from_directory(get_appyter_directory('profiles/default/static'), path=filename)

@route_join_with_or_without_slash(core, '<path:path>', methods=['GET'])
def data_files(path):
  if path.endswith('/'):
    mimetype = request.accept_mimetypes.best_match([
      'text/html',
      'application/json',
      'application/vnd.jupyter',
    ], 'text/html')
    if mimetype == 'text/html':
      fs = Filesystem(current_app.config['CWD'])
      env = get_jinja2_env(config=current_app.config)
      return env.get_template('landing.j2').render(
        _nb=os.path.basename(current_app.config['IPYNB']),
      )
    else:
      data_fs = Filesystem(Filesystem.join(current_app.config['DATA_DIR'], 'output'))
      path += current_app.config['IPYNB']
      if data_fs.exists(path):
        return send_file(data_fs.open(path, 'rb'), attachment_filename=os.path.basename(path))
  else:
    data_fs = Filesystem(Filesystem.join(current_app.config['DATA_DIR'], 'output'))
    if data_fs.exists(path):
      return send_file(data_fs.open(path, 'rb'), attachment_filename=os.path.basename(path))
  abort(404)
