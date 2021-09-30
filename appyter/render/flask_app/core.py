import os
import traceback
from flask import Blueprint, request, redirect, abort, url_for, current_app, jsonify, make_response

from appyter.context import get_jinja2_env
from appyter.ext.fs import Filesystem
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.util import exception_as_dict
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.flask_app.util import route_join_with_or_without_slash, sha1sum_io, sha1sum_dict


core = Blueprint('__main__', __name__)

_fields = None
def get_fields():
  ''' Helper to get/cache fields even if we're on a different thread
  '''
  global _fields
  if not _fields or current_app.config['DEBUG']:
    fs = Filesystem(current_app.config['CWD'])
    with fs.open(current_app.config['IPYNB'], 'r') as fr:
      env = get_jinja2_env(config=current_app.config)
      nbtemplate = nb_from_ipynb_io(fr)
      _fields = parse_fields_from_nbtemplate(env, nbtemplate)
  return _fields

_ipynb_hash = None
def get_ipynb_hash():
  global _ipynb_hash
  if not _ipynb_hash or current_app.config['DEBUG']:
    fs = Filesystem(current_app.config['CWD'])
    _ipynb_hash = sha1sum_io(fs.open(current_app.config['IPYNB'], 'rb'))
  return _ipynb_hash

def prepare_data(req):
  data = {}
  for field in get_fields():
    for name, value in field.prepare(req).items():
      assert name not in data, 'Prepare collision'
      data[name] = value
  return data

def prepare_results(data):
  results_hash = sha1sum_dict(dict(ipynb=get_ipynb_hash(), data=data))
  data_fs = Filesystem(current_app.config['DATA_DIR'])
  results_path = Filesystem.join('output', results_hash)
  if not data_fs.exists(Filesystem.join(results_path, current_app.config['IPYNB'])):
    # construct notebook
    env = get_jinja2_env(config=current_app.config, context=data, session=results_hash)
    fs = Filesystem(current_app.config['CWD'])
    with fs.open(current_app.config['IPYNB'], 'r') as fr:
      nbtemplate = nb_from_ipynb_io(fr)
    # in case of constraint failures, we'll fail here
    nb = render_nb_from_nbtemplate(env, nbtemplate, fields=get_fields(), data=data)
    # write notebook
    nbfile = Filesystem.join(results_path, os.path.basename(current_app.config['IPYNB']))
    with data_fs.open(nbfile, 'w') as fw:
      nb_to_ipynb_io(nb, fw)
  #
  return results_hash

@route_join_with_or_without_slash(core, methods=['POST'])
def post_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/json',
  ], 'text/html')
  #
  try:
    data = prepare_data(request)
    result_hash = prepare_results(data)
    error = None
  except Exception as e:
    traceback.print_exc()
    error = exception_as_dict(e)
  #
  if mimetype in {'text/html'}:
    if error: abort(406)
    else: return redirect(url_for('__main__.data_files', path=result_hash + '/'), 303)
  elif mimetype in {'application/json'}:
    if error is not None:
      return make_response(jsonify(error=error), 406)
    else:
      return make_response(jsonify(session_id=result_hash), 200)
  else:
    abort(404)

@route_join_with_or_without_slash(core, 'ssr', methods=['POST'])
def post_ssr():
  env = get_jinja2_env(config=current_app.config)
  try:
    ctx = request.get_json()
    assert ctx['field'].endswith('Field'), 'Invalid field'
    return env.globals[ctx['field']](**ctx['args']).render()
  except Exception as e:
    return make_response(jsonify(error=exception_as_dict(e)), 406)
