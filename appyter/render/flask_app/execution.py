import os
import traceback
import functools
import nbformat as nbf
from flask import current_app, request, copy_current_request_context, session
from flask_socketio import emit

from appyter.render.flask_app.app import socketio
from appyter.render.flask_app.core import core
from appyter.render.flask_app.util import sanitize_uuid

from appyter.context import get_jinja2_env
from appyter.parse.nbtemplate import nbtemplate_from_ipynb_file
from appyter.render.nbexecutor import render_nbexecutor_from_nb
from appyter.render.ipynb import render_nb_from_nbtemplate


def cleanup(session, nb):
  ''' Write notebook
  '''
  nbf.write(nb, open(os.path.join(current_app.config['DATA_DIR'], session, os.path.basename(current_app.config['IPYNB'])), 'w'))

@socketio.on('session')
def _(data):
  print('session', data, request.sid)
  session[request.sid] = dict(session.get(request.sid, {}), _session=sanitize_uuid(data['_session']))
  print(session)

@socketio.on('disconnect')
def _():
  print('disconnect', request.sid)
  if request.sid in session:
    del session[request.sid]
  print(session)

@socketio.on('init')
def init(data):
  print('init')
  session_id = sanitize_uuid(data.get('_session'))
  session_dir = os.path.join(current_app.config['DATA_DIR'], session_id)
  if os.path.exists(os.path.join(session_dir, os.path.basename(current_app.config['IPYNB']))) and not current_app.config['DEBUG']:
    print('exists')
    emit('error', 'Notebook already exists')
    emit('redirect', f"")
  else:
    env = get_jinja2_env(config=current_app.config, context=data)
    env.globals['_session'] = session_id
    nbtemplate = nbtemplate_from_ipynb_file(
      os.path.join(current_app.config['CWD'], current_app.config['IPYNB'])
    )
    nb = render_nb_from_nbtemplate(env, nbtemplate)
    os.makedirs(session_dir, exist_ok=True)
    nbf.write(nb, open(os.path.join(session_dir, os.path.basename(current_app.config['IPYNB'])), 'w'))
    emit('status', 'Notebook created, queuing execution')
    nbexecutor = copy_current_request_context(render_nbexecutor_from_nb(env, nb))
    socketio.start_background_task(
      nbexecutor,
      emit=emit,
      session_dir=session_dir,
      cleanup=functools.partial(cleanup, session_id),
    )
