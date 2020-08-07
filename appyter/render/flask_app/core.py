import os
import uuid
import json
import shutil
from flask import Blueprint, request, redirect, abort, send_from_directory, url_for, current_app

from appyter.context import get_jinja2_env
from appyter.parse.nb import nb_from_ipynb_file, nb_to_ipynb_file
from appyter.util import secure_filename
from appyter.render.form import render_form_from_nbtemplate
from appyter.render.nbviewer import render_nbviewer_from_nb
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
from appyter.render.flask_app.util import sanitize_uuid, route_join_with_or_without_slash, collapse

core = Blueprint('__main__', __name__)

def generate_session_id():
  return '00000000-0000-0000-0000-000000000000' if current_app.config['DEBUG'] else str(uuid.uuid4())

def prepare_formdata(req, **kwargs):
  # Get form variables
  data = dict({
    k: collapse(V)
    for k, V in req.form.lists()
  }, **kwargs)
  session_id = sanitize_uuid(data.get('_session'))
  if session_id is None:
    abort(404)
    return
  session_dir = os.path.join(current_app.config['DATA_DIR'], session_id)
  # Process upload files
  for fname, fh in req.files.items():
    # Save files to datadir for session
    filename = secure_filename(fh.filename)
    os.makedirs(current_app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(session_dir, exist_ok=True)
    if filename != '':
      fh.save(os.path.join(session_dir, filename))
    data[fname] = filename
  return data

def get_index_html():
  ''' Return options as form
  '''
  env = get_jinja2_env(config=current_app.config)
  env.globals.update(
    _session=generate_session_id(),
  )
  nbtemplate = nb_from_ipynb_file(
    os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
  )
  return render_form_from_nbtemplate(env, nbtemplate)

def get_index_json():
  ''' Return options as json
  '''
  env = get_jinja2_env(config=current_app.config)
  nbtemplate = nb_from_ipynb_file(
    os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
  )
  return json.dumps(render_nbtemplate_json_from_nbtemplate(env, nbtemplate))

def get_session_html_static(session_id):
  nbfile = os.path.join(current_app.config['DATA_DIR'], session_id, os.path.basename(current_app.config['IPYNB']))
  if os.path.exists(nbfile):
    nb = nb_from_ipynb_file(nbfile)
    env = get_jinja2_env(config=current_app.config)
    return env.get_template(
      'static.j2',
    ).render(
      _nb=os.path.basename(current_app.config['IPYNB']),
      _nbviewer=render_nbviewer_from_nb(env, nb),
      _session=session_id, # NOTE: this should not be necessary..
    )
  else:
    abort(404)

def get_session_ipynb_static(session_id):
  session_path = os.path.realpath(os.path.join(current_app.config['DATA_DIR'], session_id))
  return send_from_directory(
    session_path,
    os.path.basename(current_app.config['IPYNB'])
  )

def post_index_html_dynamic(data):
  ''' Return dynamic nbviewer
  '''
  env = get_jinja2_env(config=current_app.config, context=data)
  session_id = data.get('_session')
  env.globals['_session'] = session_id
  session_dir = os.path.join(current_app.config['DATA_DIR'], session_id)
  nbtemplate = nb_from_ipynb_file(os.path.join(current_app.config['CWD'], current_app.config['IPYNB']))
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  nbfile = os.path.join(session_dir, os.path.basename(current_app.config['IPYNB']))
  if not os.path.exists(nbfile) or current_app.config['DEBUG']:
    os.makedirs(session_dir, exist_ok=True)
    nb_to_ipynb_file(nb, nbfile)
  else:
    # TODO: don't do this if it's a duplicate
    # copy the current session info to a new one
    new_session_id = generate_session_id()
    env.globals['_session'] = new_session_id
    new_session_dir = os.path.join(current_app.config['DATA_DIR'], new_session_id)
    new_nbfile = os.path.join(new_session_dir, os.path.basename(current_app.config['IPYNB']))
    # TODO: only copy relevant things, i.e. not leftover files
    shutil.copytree(session_dir, new_session_dir)
    # remove nbfile so it can be recreated after redirect
    os.remove(new_nbfile)
    # redirect client to new session
    return redirect(url_for('__main__.post_index', session=new_session_id), 307)
  #
  return env.get_template(
    'dynamic.j2',
  ).render(
    _nb=os.path.basename(current_app.config['IPYNB']),
    _nbviewer=render_nbviewer_from_nb(env, nb),
    _data=json.dumps(data),
  )

def post_index_html_static(data):
  ''' Return static nbviewer
  '''
  env = get_jinja2_env(config=current_app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nb_from_ipynb_file(
    os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return env.get_template(
    'static.j2',
  ).render(
    _nbviewer=render_nbviewer_from_nb(env, nb),
    _data=json.dumps(data),
  )

def post_index_json_static(data):
  ''' Return rendered json
  '''
  env = get_jinja2_env(config=current_app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nb_from_ipynb_file(
    os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return json.dumps(render_nbtemplate_json_from_nbtemplate(env, nb))

def post_index_ipynb_static(data):
  ''' Return rendered ipynb
  '''
  env = get_jinja2_env(config=current_app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nb_from_ipynb_file(
    os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return render_nb_from_nbtemplate(env, nb)


@route_join_with_or_without_slash(core, methods=['GET', 'POST'])
def get_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
    'application/json',
  ], 'text/html')
  if request.method == 'GET':
    if mimetype in {'text/html'}:
      return get_index_html()
    elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
      env = get_jinja2_env(config=current_app.config)
      nbtemplate = nb_from_ipynb_file(
        os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
      )
      return nbtemplate
    elif mimetype in {'application/json'}:
      return get_index_json()
  elif request.method == 'POST':
    return post_index(generate_session_id())
  abort(404)

@route_join_with_or_without_slash(core, 'favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(current_app.config['STATIC_DIR'], 'favicon.ico')

@route_join_with_or_without_slash(core, '<string:session>', methods=['GET', 'POST'])
def post_index(session):
  session_id = sanitize_uuid(session)
  if session_id is None:
    abort(404)
    return
  else:
    mimetype = request.accept_mimetypes.best_match([
      'text/html',
      'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
      'application/json',
    ], 'text/html')
    if request.method == 'GET':
      if mimetype in {'text/html'}:
        return get_session_html_static(session_id)
      elif mimetype in {'application/json', 'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
        return get_session_ipynb_static(session_id)
    elif request.method == 'POST':
      if mimetype in {'text/html'}:
        if request.args.get('static') is not None:
          return post_index_html_static(prepare_formdata(request, _session=session_id))
        else:
          return post_index_html_dynamic(prepare_formdata(request, _session=session_id))
      elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
        return post_index_ipynb_static(dict(request.form.to_dict(), _session=session_id))
      elif mimetype in {'application/json'}:
        return post_index_json_static(dict(request.form.to_dict(), _session=session_id))
    abort(404)

@route_join_with_or_without_slash(core, '<string:session>', '<path:path>', methods=['GET'])
def send_session_directory(session, path):
  session_id = sanitize_uuid(session)
  if session_id is None:
    abort(404)
    return
  session_path = os.path.realpath(os.path.join(current_app.config['DATA_DIR'], session_id))
  return send_from_directory(session_path, path)
