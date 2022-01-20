import traceback
import fsspec
from flask import Blueprint, request, redirect, abort, url_for, current_app, jsonify, make_response

from appyter.context import get_jinja2_env
from appyter.ext.dict import dict_collision_free_update
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.urllib import join_url
from appyter.parse.nb import nb_to_ipynb_io
from appyter.ext.exceptions import exception_as_dict
from appyter.render.flask_app.constants import get_fields, get_deep_fields, get_ipynb_hash, get_j2_env, get_nbtemplate
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.ext.flask import route_join_with_or_without_slash
from appyter.ext.hashlib import sha1sum_dict

core = Blueprint('__main__', __name__)

def prepare_data(req):
  data = {}
  for field in get_fields():
    dict_collision_free_update(data, **field.prepare(req))
  return data

def prepare_results(data):
  results_hash = sha1sum_dict(dict(ipynb=get_ipynb_hash(), data=data))
  with url_to_chroot_fs(join_url('storage://output/', results_hash)) as data_fs:
    if not data_fs.exists(current_app.config['IPYNB']):
      # construct notebook
      env = get_jinja2_env(config=current_app.config, context=data, session=results_hash)
      nbtemplate = get_nbtemplate()
      # in case of constraint failures, we'll fail here
      nb = render_nb_from_nbtemplate(env, nbtemplate, deep_fields=get_deep_fields(), data=data)
      # write notebook
      with data_fs.open(current_app.config['IPYNB'], 'w') as fw:
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
  env = get_j2_env()
  try:
    ctx = request.get_json()
    assert ctx['field'].endswith('Field'), 'Invalid field'
    return env.globals[ctx['field']](**ctx['args']).render()
  except Exception as e:
    return make_response(jsonify(error=exception_as_dict(e)), 406)
