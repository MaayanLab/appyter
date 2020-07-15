import os
import traceback
import functools
import sys
from subprocess import Popen, PIPE
from flask import current_app, request, copy_current_request_context, session, abort
from flask_socketio import emit

from appyter.render.flask_app import socketio
from appyter.render.flask_app.core import core
from appyter.render.flask_app.util import sanitize_uuid

from appyter.context import get_jinja2_env
from appyter.render.nbconstruct import render_nb_from_nbtemplate


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
  if session_id is None:
    abort(404)
    return
  session_dir = os.path.join(current_app.config['DATA_DIR'], session_id)
  emit('status', 'Notebook created, queuing execution')
  if not current_app.config['DEBUG']:
    from eventlet.green.subprocess import Popen
  socketio.start_background_task(
    copy_current_request_context(nbexecute),
    cwd=session_dir,
    ipynb=current_app.config['IPYNB'],
    emit=emit,
    Popen=Popen,
  )

def nbexecute(cwd='', ipynb='', emit=print, Popen=Popen):
  import json
  proc = Popen(
    [
      sys.executable,
      '-u',
      '-m', 'appyter',
      'nbexecute',
      '--cwd='+cwd,
      ipynb,
    ],
    env=dict(
      PYTHONPATH=':'.join(sys.path),
      PATH=os.environ['PATH'],
    ),
    stdout=PIPE,
  )
  packet = proc.stdout.readline()
  while packet:
    msg = json.loads(packet)
    emit(msg['type'], msg['data'])
    socketio.sleep(0)
    packet = proc.stdout.readline()
