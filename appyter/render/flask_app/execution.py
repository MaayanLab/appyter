import os
import sys
import json
import uuid
import shutil
import traceback
import functools
import urllib.request
from subprocess import PIPE
from flask import current_app, request, copy_current_request_context, abort
from flask_socketio import emit

from appyter.render.flask_app.core import core, prepare_data, prepare_results
from appyter.render.flask_app.socketio import socketio, join_room, leave_room
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.flask_app.util import sanitize_sha1sum, generate_uuid, secure_filename

from appyter.context import get_jinja2_env
from appyter.util import join_routes

@socketio.on('connect')
def _():
  print('connect', request.sid)

@socketio.on('disconnect')
def _():
  print('disconnect', request.sid)

# construct/join a notebook
@socketio.on('submit')
def submit(data):
  if type(data) == dict:
    data = prepare_data(data)
    result_hash = prepare_results(data)
  elif type(data) == str:
    result_hash = sanitize_sha1sum(data)
    assert result_hash is not None
  else:
    raise Exception('Unrecognized data type')
  #
  # TODO: submit job iff it hasn't already been executed
  join_room(result_hash)
  emit('status', 'Notebook created, queuing execution', room=result_hash)
  # TODO: worry about inaccessible dispatcher
  job = dict(
    url=join_routes(request.base_url, current_app.config['PREFIX'], 'socket.io')[1:], # TODO: use public_url env
    ipynb=current_app.config['IPYNB'],
    session=result_hash,
    job=generate_uuid(),
  )
  if current_app.config['DISPATCHER']:
    queue_size = int(urllib.request.urlopen(
      urllib.request.Request(
        current_app.config['DISPATCHER'],
        method='POST',
        headers={
          'Content-Type': 'application/json',
        },
      ),
      data=json.dumps(job).encode(),
    ).read().decode())
    # TODO: keep track of queue position?
    emit('status', f"Queued successfully, you are at position {queue_size} in the queue", room=session_id)
  else:
    from appyter.orchestration.dispatch.native import dispatch
    if current_app.config['DEBUG']:
      from subprocess import Popen
    else:
      from eventlet.green.subprocess import Popen
    socketio.start_background_task(dispatch, job=job, Popen=Popen)

@socketio.on('join')
def _(data):
  session = data['session']
  job = data['job']
  join_room(session)
  emit('joined', job, room=session)

@socketio.on('message')
def _(data):
  emit(data['type'], data['data'], room=data['session'])
