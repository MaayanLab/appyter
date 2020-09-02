from queue import Queue
import functools
import importlib
from flask import Blueprint, request, current_app, jsonify

from appyter.orchestration.dispatcher.socketio import socketio

# NOTE: This is questionable, this queue may run
#       on a different thread or process; in the case of a thread it's fine
#       because Queue is thread-safe, but not in the case of a process
#       we'd need a monkey-patched redis-Queue.
#
dispatch_queue = Queue()

core = Blueprint('__main__.dispatcher', __name__)

@core.route('/', methods=['GET', 'POST'])
def on_submit():
  if request.method == 'GET':
    return f"Appyter {current_app.config['DISPATCH']} dispatcher"
  elif request.method == 'POST':
    dispatch_queue.put(dict(request.json, debug=current_app.config['DEBUG']))
    return jsonify(dispatch_queue.qsize())

def dispatcher(Q=None, dispatch=None):
  while True:
    while not Q.empty():
      job = Q.get()
      dispatch(job=job)
      Q.task_done()
    socketio.sleep(1)

@core.before_app_first_request
def init_disaptcher():
  print('Initializing dispatch...')
  from subprocess import Popen
  #
  dispatch = functools.partial(
    importlib.import_module(
      '..dispatch.{}'.format(current_app.config['DISPATCH']),
      __package__
    ).dispatch,
    Popen=Popen,
    namespace=current_app.config['KUBE_NAMESPACE'],
  )
  #
  print('Starting background tasks...')
  for _ in range(current_app.config['JOBS']):
    socketio.start_background_task(dispatcher, Q=dispatch_queue, dispatch=dispatch)

