import logging
import traceback
from flask import Blueprint, request, redirect, abort, url_for, current_app, jsonify, make_response

from appyter.ext.exceptions import exception_as_dict
from appyter.ext.flask import route_join_with_or_without_slash
from appyter.render.flask_app.constants import get_j2_env
from appyter.render.flask_app.prepare import prepare_data, prepare_request, prepare_results

logger = logging.getLogger(__name__)

core = Blueprint('__main__', __name__)

@route_join_with_or_without_slash(core, methods=['POST'])
def post_index():
  mimetype = request.accept_mimetypes.best_match([
    'text/html',
    'application/json',
  ], 'text/html')
  #
  try:
    data = dict(_config=current_app.config)
    data.update(prepare_data(request))
    data.update(prepare_request(request))
    instance_id = prepare_results(data)
    error = None
  except KeyboardInterrupt:
    raise
  except Exception as e:
    logger.error(traceback.format_exc())
    error = exception_as_dict(e)
  #
  if mimetype in {'text/html'}:
    if error: abort(406)
    else: return redirect(url_for('__main__.data_files', path=instance_id + '/', executor=data.get('_executor'), storage=data.get('_storage')), 303)
  elif mimetype in {'application/json'}:
    if error is not None:
      return make_response(jsonify(error=error), 406)
    else:
      # NOTE: Legacy session_id preserved but deprecated
      ret = dict(_id=instance_id, session_id=instance_id)
      if data.get('_executor'): ret.update(_executor=data['_executor'])
      if data.get('_storage'): ret.update(_storage=data['_storage'])
      return make_response(jsonify(ret), 200)
  else:
    abort(404)

@route_join_with_or_without_slash(core, 'ssr', methods=['POST'])
def post_ssr():
  env = get_j2_env()
  try:
    ctx = request.get_json()
    assert ctx['field'].endswith('Field'), 'Invalid field'
    return env.globals[ctx['field']](**ctx['args']).render()
  except KeyboardInterrupt:
    raise
  except Exception as e:
    return make_response(jsonify(error=exception_as_dict(e)), 406)
