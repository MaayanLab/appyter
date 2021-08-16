import os
import uuid
import json
import traceback
from flask import Blueprint, request, redirect, abort, send_file, url_for, current_app, jsonify, make_response
from werkzeug.exceptions import BadRequest

from appyter.context import get_jinja2_env
from appyter.ext.fs import Filesystem
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.util import secure_filepath, exception_as_dict
from appyter.render.form import render_form_from_nbtemplate
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
from appyter.render.flask_app.download import upload_from_request
from appyter.render.flask_app.util import sanitize_sha1sum, sanitize_uuid, route_join_with_or_without_slash, collapse, sha1sum_io, sha1sum_dict


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
      _fields = render_nbtemplate_json_from_nbtemplate(env, nbtemplate)
  return _fields

_ipynb_hash = None
def get_ipynb_hash():
  global _ipynb_hash
  if not _ipynb_hash or current_app.config['DEBUG']:
    fs = Filesystem(current_app.config['CWD'])
    _ipynb_hash = sha1sum_io(fs.open(current_app.config['IPYNB'], 'rb'))
  return _ipynb_hash

def prepare_data(data):
  # Assert that all fields are accounted for
  fields = {field['args']['name'] for field in get_fields()}
  unrecognized = set(data.keys()) - fields
  if unrecognized:
    raise BadRequest(f"Unrecognized fields: {', '.join(unrecognized)}")
  return data

def prepare_formdata(req):
  ''' Get data defined for each field from json/form. Also process POSTed files
  '''
  fields = get_fields()
  file_fields = {
    field['args']['name']
    for field in fields
    if field['field'] == 'FileField'
  }
  data = {}
  if req.form:
    data.update({
      field['args']['name']: collapse(req.form.getlist(field['args']['name']))
      for field in fields
      if field['args']['name'] in req.form
    })
    data.update(upload_from_request(req, file_fields))
  elif req.json:
    data.update({
      field['args']['name']: req.json.get(field['args']['name'])
      for field in fields
      if field['args']['name'] in req.json
    })
  return prepare_data(data)

def prepare_results(data):
  results_hash = sha1sum_dict(dict(ipynb=get_ipynb_hash(), data=data))
  data_fs = Filesystem(current_app.config['DATA_DIR'])
  results_path = Filesystem.join('output', results_hash)
  if not data_fs.exists(Filesystem.join(results_path, current_app.config['IPYNB'])):
    # prepare files to be linked and update field to use filename
    file_fields = {
      field['args']['name']
      for field in get_fields()
      if field['field'] == 'FileField'
    }
    links = []
    files = {}
    for file_field in file_fields:
      if fdata := data.get(file_field):
        content_hash, filename = fdata.split('/', maxsplit=1)
        content_hash = sanitize_sha1sum(content_hash)
        filename = secure_filepath(filename)
        links.append((
          Filesystem.join('input', content_hash),
          Filesystem.join(results_path, filename)
        ))
        files[filename] = filename
        data[file_field] = filename
    # construct notebook
    env = get_jinja2_env(config=current_app.config, context=data, session=results_hash)
    fs = Filesystem(current_app.config['CWD'])
    with fs.open(current_app.config['IPYNB'], 'r') as fr:
      nbtemplate = nb_from_ipynb_io(fr)
    # in case of constraint failures, we'll fail here
    nb = render_nb_from_nbtemplate(env, nbtemplate, files=files)
    # actually link all input files into output directory
    for src, dest in links:
      data_fs.link(src, dest)
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
    data = prepare_formdata(request)
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
