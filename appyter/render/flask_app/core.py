import os
import uuid
import json
from flask import Blueprint, request, redirect, abort, send_file, send_from_directory, url_for, current_app, jsonify

from appyter.context import get_jinja2_env, get_profile_directory
from appyter.parse.nb import nb_from_ipynb_file, nb_to_ipynb_file
from appyter.util import secure_filename
from appyter.render.form import render_form_from_nbtemplate
from appyter.render.nbviewer import render_nbviewer_from_nb
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
from appyter.render.flask_app.download import upload_from_request
from appyter.render.flask_app.util import sanitize_uuid, route_join_with_or_without_slash, collapse, sha1sum_file, sha1sum_dict


core = Blueprint('__main__', __name__)

@core.before_app_first_request
def prerender():
  ''' Pre-render certain pages for quicker access / direct access via nginx in production
  '''
  env = get_jinja2_env(config=current_app.config)
  nbtemplate = nb_from_ipynb_file(current_app.config['IPYNB'])
  with open(os.path.join(current_app.config['DATA_DIR'], 'index.html'), 'w') as fw:
    fw.write(render_form_from_nbtemplate(env, nbtemplate))
  with open(os.path.join(current_app.config['DATA_DIR'], 'index.json'), 'w') as fw:
    json.dump(render_nbtemplate_json_from_nbtemplate(env, nbtemplate), fw)
  env.get_template(
    'landing.j2',
  ).stream(
    _nb=os.path.basename(current_app.config['IPYNB']),
  ).dump(
    os.path.join(current_app.config['DATA_DIR'], 'landing.html')
  )

_fields = None
def get_fields():
  ''' Helper to get/cache fields even if we're on a different thread
  '''
  global _fields
  if not _fields:
    with open(os.path.join(current_app.config['DATA_DIR'], 'index.json'), 'r') as fr:
      _fields = json.load(fr)
  return _fields

_ipynb_hash = None
def get_ipynb_hash():
  global _ipynb_hash
  if not _ipynb_hash:
    _ipynb_hash = sha1sum_file(os.path.join(current_app.config['CWD'], current_app.config['IPYNB']))
  return _ipynb_hash

def prepare_data(data):
  # TODO: assert constraints
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
      field['args']['name']: collapse(V)
      for field in fields
      for V in req.form.getlist(field['args']['name'])
      if field['args']['name'] in req.form
    })
    data.update(upload_from_request(req, file_fields))
  elif req.json:
    data.update({
      field['args']['name']: v
      for field in fields
      for v in req.json.get(field['args']['name'])
      if field['args']['name'] in req.json
    })
  return prepare_data(data)

def prepare_results(data):
  results_hash = sha1sum_dict(dict(ipynb=get_ipynb_hash(), data=data))
  results_path = os.path.join(current_app.config['DATA_DIR'], 'output', results_hash)
  if not os.path.exists(results_path):
    fields = get_fields()
    file_fields = {
      field['args']['name']
      for field in fields
      if field['field'] == 'FileField'
    }
    # link all input files into output directory
    for file_field in file_fields:
      if fdata := data.get(file_field):
        os.link(
          os.path.join(current_app.config['DATA_DIR'], 'input', fdata['content_hash']),
          os.path.join(results_path, secure_filename(fdata['filename']))
        )
        fdata = secure_filename(fdata['filename'])
    # construct/write landing page
    os.link(
      os.path.join(current_app.config['DATA_DIR'], 'landing.html'),
      os.path.join(results_path, 'index.html')
    )
    # construct/write notebook
    env = get_jinja2_env(config=current_app.config, context=data)
    nbtemplate = nb_from_ipynb_file(os.path.join(current_app.config['CWD'], current_app.config['IPYNB']))
    nb = render_nb_from_nbtemplate(env, nbtemplate)
    nbfile = os.path.join(results_path, os.path.basename(current_app.config['IPYNB']))
    nb_to_ipynb_file(nb, nbfile)
  #
  return results_hash

@route_join_with_or_without_slash(core, methods=['POST'])
def post_index():
  data = prepare_formdata(request)
  result_hash = prepare_results(data)
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/json',
  ], 'text/html')
  if mimetype in {'text/html'}:
    return redirect(url_for('static_data', path=result_hash))
  elif mimetype in {'application/json'}:
    return jsonify(dict(session_id=result_hash))
  else:
    abort(404)
