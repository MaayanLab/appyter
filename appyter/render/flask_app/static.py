''' Represent the areas that can be handled externally in production
'''
import os
from flask import request, current_app, send_file, send_from_directory, abort, jsonify
from werkzeug.exceptions import NotFound

from appyter.ext.urllib import URI, join_url
from appyter.render.flask_app.constants import get_form, get_ipynb_io, get_nbtemplate_json, get_static_fs, get_j2_env
from appyter.render.flask_app.core import core
from appyter.ext.flask import route_join_with_or_without_slash
from appyter.context import get_appyter_directory
from appyter.ext.contextlib import ContextManagerAsHandle
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.render.flask_app.prepare import prepare_request, prepare_storage

@route_join_with_or_without_slash(core, methods=['GET'])
def get_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/json',
    'application/vnd.jupyter',
  ], 'text/html')
  if mimetype in {'text/html'}:
    return get_form()
  elif mimetype in {'application/json'}:
    return jsonify(get_nbtemplate_json())
  elif mimetype in {'application/vnd.jupyter'}:
    return send_file(get_ipynb_io(), attachment_filename=current_app.config['IPYNB'], mimetype=mimetype)
  else:
    abort(404)

@core.route('/favicon.ico', methods=['GET'])
def favicon():
  static = get_static_fs()
  if static.exists('favicon.ico'):
    return send_file(static.open('favicon.ico', 'rb'), attachment_filename='favicon.ico')
  abort(404)

@core.route('/static/<path:filename>', methods=['GET'])
def static(filename):
  static = get_static_fs()
  if static.exists(filename):
    return send_file(static.open(filename, 'rb'), attachment_filename=filename)
    #
  try:
    return send_from_directory(get_appyter_directory('static'), path=filename)
  except:
    try:
      return send_from_directory(get_appyter_directory(f"static/profiles/{current_app.config['PROFILE']}"), path=filename)
    except NotFound:
      return send_from_directory(get_appyter_directory('static/profiles/default'), path=filename)

@route_join_with_or_without_slash(core, '<path:path>', methods=['GET'])
def data_files(path):
  data = prepare_request(request)
  #
  if path.endswith('/'):
    mimetype = request.accept_mimetypes.best_match([
      'text/html',
      'application/json',
      'application/vnd.jupyter',
    ], 'text/html')
    if mimetype == 'text/html':
      return get_j2_env().get_template('landing.j2').render(
        _nb=current_app.config['IPYNB'],
      )
    else:
      output_fs_ctx = ContextManagerAsHandle(url_to_chroot_fs(str(URI(prepare_storage(data)).join('output'))))
      output_fs = output_fs_ctx.open()
      path = join_url(path, current_app.config['IPYNB'])
      if output_fs.exists(path):
        response = send_file(output_fs.open(path, 'rb'), attachment_filename=current_app.config['IPYNB'])
        response.call_on_close(output_fs_ctx.close)
        return response
      else:
        output_fs_ctx.close()
  else:
    output_fs_ctx = ContextManagerAsHandle(url_to_chroot_fs(str(URI(prepare_storage(data)).join('output'))))
    output_fs = output_fs_ctx.open()
    if output_fs.exists(path):
      response = send_file(output_fs.open(path, 'rb'), attachment_filename=os.path.basename(path))
      response.call_on_close(output_fs_ctx.close)
      return response
    else:
      output_fs_ctx.close()

  abort(404)
