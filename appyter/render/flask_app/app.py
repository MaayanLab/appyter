import os
import uuid
import json
import shutil
import nbformat as nbf
from functools import partial
from queue import Queue
from flask import Flask, request, abort, copy_current_request_context, send_from_directory
from flask_socketio import SocketIO, emit
from appyter.context import get_sys_env, get_jinja2_env, get_extra_files
from appyter.parse.nbtemplate import nbtemplate_from_ipynb_file
from appyter.render.form import render_form_from_nbtemplate
from appyter.render.nbviewer import render_nbviewer_from_nb
from appyter.render.ipynb import render_nb_from_nbtemplate
from appyter.render.json import render_nbtemplate_json_from_nbtemplate
from appyter.render.nbexecutor import render_nbexecutor_from_nb
from werkzeug.utils import secure_filename

# Prepare environment
from dotenv import load_dotenv
load_dotenv()
args, kargs, kwargs = get_sys_env()

PREFIX = kwargs.get('prefix', os.environ.get('PREFIX', '/'))
HOST = kwargs.get('host', os.environ.get('HOST', '127.0.0.1'))
PORT = json.loads(kwargs.get('port', os.environ.get('PORT', '5000')))
PROXY = json.loads(kwargs.get('proxy', os.environ.get('PROXY', 'false')))
CWD = kwargs.get('cwd', os.environ.get('CWD', os.curdir))
DATA_DIR = kwargs.get('data-dir', os.environ.get('DATA_DIR', 'data'))
MAX_THREADS = json.loads(kwargs.get('max-threads', os.environ.get('MAX_THREADS', '10')))
SECRET_KEY = kwargs.get('secret-key', os.environ.get('SECRET_KEY', str(uuid.uuid4())))
DEBUG = json.loads(kwargs.get('debug', os.environ.get('DEBUG', 'true')))
STATIC_DIR = kwargs.get('static-dir', os.path.abspath(os.path.join(CWD, 'static')))
IPYNB = args[0] if len(args) > 0 else os.environ.get('APP', 'app.ipynb')
SHOW_HELP = 'h' in kargs or 'help' in kwargs or args == []
STATIC_PREFIX = '/' + '/'.join(filter(None, [*PREFIX.split('/'), 'static']))

# Prepare app
app = Flask(__name__, static_url_path=STATIC_PREFIX, static_folder=STATIC_DIR)
app.config['SECRET_KEY'] = SECRET_KEY
socketio = SocketIO(app,
  path=f"{PREFIX}socket.io",
  async_mode='threading',
  logger=DEBUG,
  engineio_logger=DEBUG,
  cors_allowed_origins='*',
)
if PROXY:
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
    socketio.start_background_task(fn, **kwargs)
    execution_queue.task_done()

@app.before_first_request
def init_app():
  os.makedirs(DATA_DIR, exist_ok=True)
  print('Spawning workers...')
  for n in range(n_workers):
    socketio.start_background_task(worker, n=n, execution_queue=execution_queue)

# Util
def sanitize_uuid(val):
  return str(uuid.UUID(val))

def route_join_with_or_without_slash(app, *routes, **kwargs):
  ''' Like @app.route but doesn't care about trailing slash or not
  '''
  def wrapper(func):
    routes_stripped = '/'.join([route.strip('/') for route in routes if route.strip('/')])
    if routes_stripped:
      app.route('/' + routes_stripped, **kwargs)(func)
    app.route('/' + routes_stripped + '/', **kwargs)(func)
    return func
  return wrapper

def get_index_html():
  ''' Return options as form
  '''
  env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG)
  env.globals.update(
    _session=str('00000000-0000-0000-0000-000000000000' if DEBUG else uuid.uuid4())
  )
  nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
  return render_form_from_nbtemplate(env, nbtemplate)

def get_index_json():
  ''' Return options as json
  '''
  env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG)
  nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
  return render_nbtemplate_json_from_nbtemplate(env, nbtemplate)

def get_session_html_static(session_id):
  nbfile = os.path.join(DATA_DIR, session_id, os.path.basename(IPYNB))
  if os.path.exists(nbfile):
    nb = nbf.read(open(nbfile, 'r'), as_version=4)
    env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG)
    return env.get_template(
      'static.j2',
    ).render(
      _nb=os.path.basename(IPYNB),
      _nbviewer=render_nbviewer_from_nb(env, nb),
      _session=session_id, # NOTE: this should not be necessary..
    )
  else:
    abort(404)

def get_session_ipynb_static(session_id):
  # TODO: if still executing, flush current state
  nbfile = os.path.join(DATA_DIR, session_id, os.path.basename(IPYNB))
  if os.path.exists(nbfile):
    return send_from_directory(os.path.join(DATA_DIR, session_id), os.path.basename(IPYNB))
  else:
    abort(404)

def post_index_html_dynamic(data):
  ''' Return dynamic nbviewer
  '''
  env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG, context=data)
  nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return env.get_template(
    'dynamic.j2',
  ).render(
    _nb=os.path.basename(IPYNB),
    _nbviewer=render_nbviewer_from_nb(env, nb),
    _data=json.dumps(data),
    _session=data['_session'], # NOTE: this should not be necessary..
  )

def post_index_html_static(data):
  ''' Return static nbviewer
  '''
  env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG, context=data)
  nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return env.get_template(
    'static.j2',
  ).render(
    _nbviewer=render_nbviewer_from_nb(env, nb),
    _data=json.dumps(data),
    _session=data['_session'], # NOTE: this should not be necessary..
  )

def post_index_json_static(data):
  ''' Return rendered json
  '''
  env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG, context=data)
  nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  return render_nbtemplate_json_from_nbtemplate(env, nb)

def post_index_ipynb_static(data):
  ''' Return rendered ipynb
  '''
  env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG, context=data)
  nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
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
  session_dir = os.path.join(DATA_DIR, session_id)
  # Process upload files
  for fname, fh in req.files.items():
    # Save files to datadir for session
    filename = secure_filename(fh.filename)
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(session_dir, exist_ok=True)
    if filename != '':
      fh.save(os.path.join(session_dir, filename))
    data[fname] = filename
  return data

@route_join_with_or_without_slash(app, PREFIX, methods=['GET'])
def get_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json',
    'application/json',
  ], 'text/html')
  if mimetype in {'text/html'}:
    return get_index_html()
  elif mimetype in {'application/vnd.jupyter', 'application/vnd.jupyter.cells', 'application/x-ipynb+json'}:
    env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG)
    nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
    return nbtemplate
  elif mimetype in {'application/json'}:
    return get_index_json()
  abort(404)

@route_join_with_or_without_slash(app, PREFIX, 'favicon.ico', methods=['GET'])
def favicon():
  return send_from_directory(STATIC_DIR, 'favicon.ico')

@route_join_with_or_without_slash(app, PREFIX, '<string:session>', methods=['GET', 'POST'])
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

@route_join_with_or_without_slash(app, PREFIX, '<string:session>', '<path:path>', methods=['GET'])
def send_session_directory(session, path):
  session_id = sanitize_uuid(session)
  session_path = os.path.realpath(os.path.join(DATA_DIR, session_id))
  return send_from_directory(session_path, path)

def cleanup(session, nb):
  ''' Write notebook
  '''
  nbf.write(nb, open(os.path.join(DATA_DIR, session, os.path.basename(IPYNB)), 'w'))

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
  session_dir = os.path.join(DATA_DIR, session_id)
  if os.path.exists(os.path.join(session_dir, os.path.basename(IPYNB))) and not DEBUG:
    print('exists')
    emit('error', 'Notebook already exists')
    emit('redirect', f"")
  else:
    env = get_jinja2_env(cwd=CWD, prefix=PREFIX, debug=DEBUG, context=data)
    nbtemplate = nbtemplate_from_ipynb_file(env.globals['_args'][0])
    nb = render_nb_from_nbtemplate(env, nbtemplate)
    os.makedirs(session_dir, exist_ok=True)
    nbf.write(nb, open(os.path.join(session_dir, os.path.basename(IPYNB)), 'w'))
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

@socketio.on("siofu_start")
def siofu_start(data):
  print('file upload start')
  global session
  session_id = session[request.sid]['_session']
  session_dir = os.path.join(DATA_DIR, session_id)
  filename = secure_filename(data.get('name'))
  os.makedirs(DATA_DIR, exist_ok=True)
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
  if SHOW_HELP:
    do_help()
  else:
    return socketio.run(
        app,
        host=HOST,
        port=PORT,
        debug=DEBUG,
        use_reloader=DEBUG,
        extra_files=get_extra_files(),
    )

if __name__ == '__main__':
  main()
