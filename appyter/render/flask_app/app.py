import os
import uuid
import json
import shutil
import nbformat as nbf
import traceback
import urllib.request, urllib.parse
from functools import partial
from queue import Queue
from flask import Flask, Blueprint, request, abort, copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit
from appyter.context import get_env, get_jinja2_env, get_extra_files, find_blueprints
from appyter.parse.nbtemplate import nbtemplate_from_ipynb_file
from appyter.render.form import render_form_from_nbtemplate
from appyter.render.nbviewer import render_nbviewer_from_nb
from appyter.render.ipynb import render_nb_from_nbtemplate
from appyter.render.json import render_nbtemplate_json_from_nbtemplate
from appyter.render.nbexecutor import render_nbexecutor_from_nb
from appyter.util import join_routes
from werkzeug.utils import secure_filename

# Prepare environment
config = get_env()

# https://github.com/pallets/flask/issues/3209#issuecomment-494008394
os.environ['FLASK_SKIP_DOTENV'] = '1'

# Prepare app
app = Flask(__name__, static_url_path=config['STATIC_PREFIX'], static_folder=config['STATIC_DIR'])
core = Blueprint('__main__', __name__)
app.config.update(config)
socketio = SocketIO(app,
  path=f"{config['PREFIX']}socket.io",
  async_mode='threading',
  logger=config['DEBUG'],
  engineio_logger=config['DEBUG'],
  cors_allowed_origins='*',
)
if app.config['PROXY']:
  from werkzeug.middleware.proxy_fix import ProxyFix
  app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

session = {}
execution_queue = Queue()

# Prepare background workers
n_workers = 10

def worker(n, execution_queue):
  while True:
    fn, kwargs = execution_queue.get()
    print(f"worker {n}: {fn}({kwargs})")
    try:
      fn(**kwargs)
    except Exception as e:
      print(f"worker {n} error")
      traceback.print_exc()
    execution_queue.task_done()

@app.before_first_request
def init_app():
  os.makedirs(app.config['DATA_DIR'], exist_ok=True)
  print('Spawning workers...')
  for n in range(n_workers):
    socketio.start_background_task(worker, n=n, execution_queue=execution_queue)

# Util
def sanitize_uuid(val):
  return str(uuid.UUID(val))

def secure_url(url):
  parsed = urllib.parse.urlparse(url)
  assert parsed.scheme in {'https', 'http', 'ftp'}, 'Invalid scheme'
  return url

def route_join_with_or_without_slash(blueprint, *routes, **kwargs):
  ''' Like @app.route but doesn't care about trailing slash or not
  '''
  def wrapper(func):
    routes_stripped = join_routes(*routes)
    if routes_stripped:
      blueprint.route(routes_stripped, **kwargs)(func)
    blueprint.route(routes_stripped + '/', **kwargs)(func)
    return func
  return wrapper

def get_index_html():
  ''' Return options as form
  '''
  env = get_jinja2_env(app.config)
  env.globals.update(
    _session=str('00000000-0000-0000-0000-000000000000' if app.config['DEBUG'] else uuid.uuid4())
  )
  nbtemplate = nbtemplate_from_ipynb_file(
    os.path.join(app.config['CWD'], app.config['ARGS'][0])
  )
  return render_form_from_nbtemplate(env, nbtemplate)

def get_index_json():
  ''' Return options as json
  '''
  env = get_jinja2_env(app.config)
  nbtemplate = nbtemplate_from_ipynb_file(
    os.path.join(app.config['CWD'], app.config['ARGS'][0])
  )
  return render_nbtemplate_json_from_nbtemplate(env, nbtemplate)

def get_session_html_static(session_id):
  nbfile = os.path.join(app.config['DATA_DIR'], session_id, os.path.basename(app.config['IPYNB']))
  if os.path.exists(nbfile):
    nb = nbf.read(open(nbfile, 'r'), as_version=4)
    env = get_jinja2_env(config=app.config)
    return env.get_template(
      'static.j2',
    ).render(
      _nb=os.path.basename(app.config['IPYNB']),
      _nbviewer=render_nbviewer_from_nb(env, nb),
      _session=session_id, # NOTE: this should not be necessary..
    )
  else:
    abort(404)

def get_session_ipynb_static(session_id):
  # TODO: if still executing, flush current state
  nbfile = os.path.join(app.config['DATA_DIR'], session_id, os.path.basename(app.config['IPYNB']))
  if os.path.exists(nbfile):
    return send_from_directory(os.path.join(app.config['DATA_DIR'], session_id), os.path.basename(app.config['IPYNB']))
  else:
    abort(404)

def post_index_html_dynamic(data):
  ''' Return dynamic nbviewer
  '''
  env = get_jinja2_env(config=app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nbtemplate_from_ipynb_file(
    os.path.join(app.config['CWD'], app.config['ARGS'][0])
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return env.get_template(
    'dynamic.j2',
  ).render(
    _nb=os.path.basename(app.config['IPYNB']),
    _nbviewer=render_nbviewer_from_nb(env, nb),
    _data=json.dumps(data),
  )

def post_index_html_static(data):
  ''' Return static nbviewer
  '''
  env = get_jinja2_env(config=app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nbtemplate_from_ipynb_file(
    os.path.join(app.config['CWD'], app.config['ARGS'][0])
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
  env = get_jinja2_env(config=app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nbtemplate_from_ipynb_file(
    os.path.join(app.config['CWD'], app.config['ARGS'][0])
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return render_nbtemplate_json_from_nbtemplate(env, nb)

def post_index_ipynb_static(data):
  ''' Return rendered ipynb
  '''
  env = get_jinja2_env(config=app.config, context=data)
  env.globals['_session'] = data.get('_session')
  nbtemplate = nbtemplate_from_ipynb_file(
    os.path.join(app.config['CWD'], app.config['ARGS'][0])
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return render_nb_from_nbtemplate(env, nb)

def collapse(L):
  if len(L) == 1:
    return L[0]
  else:
    return L

def prepare_formdata(req):
  # Get form variables
  data = {
    k: collapse(V)
    for k, V in req.form.lists()
  }
  session_id = sanitize_uuid(data.get('_session'))
  session_dir = os.path.join(app.config['DATA_DIR'], session_id)
  # Process upload files
  for fname, fh in req.files.items():
    # Save files to datadir for session
    filename = secure_filename(fh.filename)
    os.makedirs(app.config['DATA_DIR'], exist_ok=True)
    os.makedirs(session_dir, exist_ok=True)
    if filename != '':
      fh.save(os.path.join(session_dir, filename))
    data[fname] = filename
  return data

@route_join_with_or_without_slash(core, methods=['GET'])
def get_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
    'application/json',
  ], 'text/html')
  if mimetype in {'text/html'}:
    return get_index_html()
  elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
    env = get_jinja2_env(config=app.config)
    nbtemplate = nbtemplate_from_ipynb_file(
      os.path.join(app.config['CWD'], app.config['ARGS'][0])
    )
    return nbtemplate
  elif mimetype in {'application/json'}:
    return get_index_json()
  abort(404)

@route_join_with_or_without_slash(core, 'favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(app.config['STATIC_DIR'], 'favicon.ico')

@route_join_with_or_without_slash(core, '<string:session>', methods=['GET', 'POST'])
def post_index(session):
  try:
    session_id = sanitize_uuid(session)
  except:
    abort(404)
  else:
    mimetype = request.accept_mimetypes.best_match([
      'text/html',
      'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
      'application/json',
    ], 'text/html')
    if request.method == 'GET':
      if mimetype in {'text/html'}:
        return get_session_html_static(session_id)
      elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
        return get_session_ipynb_static(session_id)
    elif request.method == 'POST':
      if mimetype in {'text/html'}:
        if request.args.get('static') is not None:
          return post_index_html_static(prepare_formdata(request))
        else:
          return post_index_html_dynamic(prepare_formdata(request))
      elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
        return post_index_ipynb_static(request.form.to_dict())
      elif mimetype in {'application/json'}:
        return post_index_json_static(request.form.to_dict())
    abort(404)

@route_join_with_or_without_slash(core, '<string:session>', '<path:path>', methods=['GET'])
def send_session_directory(session, path):
  session_id = sanitize_uuid(session)
  session_path = os.path.realpath(os.path.join(app.config['DATA_DIR'], session_id))
  return send_from_directory(session_path, path)

def cleanup(session, nb):
  ''' Write notebook
  '''
  nbf.write(nb, open(os.path.join(app.config['DATA_DIR'], session, os.path.basename(app.config['IPYNB'])), 'w'))

@socketio.on('session')
def _(data):
  print('session', data)
  global session
  session[request.sid] = dict(session.get(request.sid, {}), _session=sanitize_uuid(data['_session']))

@socketio.on('disconnect')
def _():
  global session
  if request.sid in session:
    del session[request.sid]

@socketio.on('init')
def init(data):
  print('init')
  session_id = sanitize_uuid(data.get('_session'))
  session_dir = os.path.join(app.config['DATA_DIR'], session_id)
  if os.path.exists(os.path.join(session_dir, os.path.basename(app.config['IPYNB']))) and not DEBUG:
    print('exists')
    emit('error', 'Notebook already exists')
    emit('redirect', f"")
  else:
    env = get_jinja2_env(config=app.config, context=data)
    env.globals['_session'] = session_id
    nbtemplate = nbtemplate_from_ipynb_file(
      os.path.join(app.config['CWD'], app.config['ARGS'][0])
    )
    nb = render_nb_from_nbtemplate(env, nbtemplate)
    os.makedirs(session_dir, exist_ok=True)
    nbf.write(nb, open(os.path.join(session_dir, os.path.basename(app.config['IPYNB'])), 'w'))
    emit('status', 'Notebook created, queuing execution')
    nbexecutor = copy_current_request_context(render_nbexecutor_from_nb(env, nb))
    execution_queue.put((
      nbexecutor,
      dict(
        emit=emit,
        session_dir=session_dir,
        cleanup=partial(cleanup, session_id),
      ),
    ))


@socketio.on('download_start')
def download(data):
  print('file download start')
  global session
  session_id = session[request.sid]['_session']
  session_dir = os.path.join(app.config['DATA_DIR'], session_id)
  os.makedirs(app.config['DATA_DIR'], exist_ok=True)
  os.makedirs(session_dir, exist_ok=True)
  name = data.get('name')
  url = secure_url(data.get('url'))
  filename = secure_filename(data.get('file'))
  # TODO: worry about files that are too big/long
  @copy_current_request_context
  def download_with_progress(name, url, path, filename, emit):
    emit('download_start', dict(name=name, filename=filename))
    try:
      urllib.request.urlretrieve(
        url, filename=path,
        reporthook=lambda chunk, chunk_size, total_size: emit(
          'download_progress', dict(
            name=name,
            chunk=chunk,
            chunk_size=chunk_size,
            total_size=total_size
          )
        ),
      )
    except Exception as e:
      print('download error')
      traceback.print_exc()
      emit('download_error', dict(name=name, filename=filename, error=str(e)))
    else:
      emit('download_complete', dict(name=name, filename=filename))
  #
  execution_queue.put((
    download_with_progress,
    dict(
      name=name,
      url=url,
      path=os.path.join(session_dir, filename),
      filename=filename,
      emit=emit,
    )
  ))
  emit('download_queued', dict(name=name, filename=filename))


@socketio.on("siofu_start")
def siofu_start(data):
  print('file upload start')
  global session
  session_id = session[request.sid]['_session']
  session_dir = os.path.join(app.config['DATA_DIR'], session_id)
  filename = secure_filename(data.get('name'))
  os.makedirs(app.config['DATA_DIR'], exist_ok=True)
  os.makedirs(session_dir, exist_ok=True)
  if filename != '':
    session[request.sid] = dict(session[request.sid], **{
      'file_%d' % (data.get('id')): dict(data,
        name=filename,
        bytesLoaded=0,
        fh=open(os.path.join(session_dir, filename), 'wb'),
      ),
    })

    emit('siofu_ready', {
      'id': data.get('id'),
      'name': None,
    })
  else:
    emit('siofu_error', 'Invalid filename')

@socketio.on("siofu_progress")
def siofu_progress(data):
  global session
  session[request.sid]['file_%d' % (data['id'])]['fh'].write(data['content'])
  emit("siofu_chunk", {
    'id': data['id'],
  })

@socketio.on("siofu_done")
def siofu_done(data):
  print('file upload complete')
  global session
  session[request.sid]['file_%d' % (data['id'])]['fh'].close()
  del session[request.sid]['file_%d' % (data['id'])]
  emit('siofu_complete', {
    'id': data['id'],
  })

@socketio.on_error()
def error_handler(e):
  print(e)

def do_help():
  print('Usage: jupyter-template [OPTIONS] <template.ipynb>')
  print('')
  print('OPTIONS')
  print('  --cwd=DIRECTORY    The directory where it should run (contains fields, templates and such)')
  print('  --profile=PROFILE  The styling profile to use see `PROFILES`')
  print('')
  print('PROFILES')
  print('  default  Bare profile with no styling')

def main():
  if app.config['SHOW_HELP']:
    do_help()
  else:
    # env preparation
    get_jinja2_env(config=app.config)

    # register additional blueprints
    app.register_blueprint(core, url_prefix=app.config['PREFIX'])
    for blueprint_name, blueprint in find_blueprints(config=app.config).items():
      if isinstance(blueprint, Blueprint):
        app.register_blueprint(blueprint, url_prefix=join_routes(app.config['PREFIX'], blueprint_name))
      elif callable(blueprint):
        blueprint(app, url_prefix=join_routes(app.config['PREFIX'], blueprint_name), DATA_DIR=app.config['DATA_DIR'])
      else:
        raise Exception('Unrecognized blueprint type: ' + blueprint_name)

    return socketio.run(
        app,
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
        use_reloader=app.config['DEBUG'],
        extra_files=get_extra_files(config=app.config),
    )

if __name__ == '__main__':
  main()
