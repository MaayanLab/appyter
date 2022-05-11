import re
from appyter.context import get_env

from appyter.ext.flask import request_get
from appyter.ext.dict import dict_filter_none

async def prepare_request(req):
  ''' Extract additional fields from request
  '''
  data = dict(_config=get_env())
  data.update(dict_filter_none({
    k: request_get(req, k)
    for k in [
      '_auth',
      '_executor',
      '_storage',
    ]
  }))
  # if executor hints are provided (e.g. ['executor:default'])
  #  we'll verify that the chosen executor is supported
  executor_hints = {
    hint_value
    for hint in data.get('_config').get('HINTS', set())
    for hint_prefix, sep, hint_value in (hint.partition(':'),)
    if hint_prefix == 'executor' and sep == ':'
  }
  if executor_hints and data.get('_executor', 'default') not in executor_hints:
    raise Exception('Executor not supported for this appyter')
  #
  if not data.get('_auth') and getattr(req, 'cookies', None) is not None:
    authorization = req.cookies.get('authorization')
    if authorization:
      data['_auth'] = authorization

  if not data.get('_auth') and getattr(req, 'headers', None) is not None:
    authorization = req.headers.get('Authorization')
    if authorization:
      m = re.match(r'^Bearer (.+)$', authorization)
      if m:
        data['_auth'] = m.group(1)
  #
  if not data.get('_storage') and getattr(req, 'args', None) is not None:
    storage = req.args.get('storage')
    if storage:
      data['_storage'] = storage
  #
  if data.get('_executor') == 'cavatica':
    # CAVATICA executor must be authenticated
    if not data.get('_auth'): raise PermissionError
    # CAVATICA executor should use cavatica storage
    if not data.get('_storage'):
      # NOTE: this gets sanitized downstream
      cavatica_project = request_get(req, '_cavatica_project')
      if not cavatica_project:
        from appyter.extras.catalog_integration.user_config import get_user_config
        user_config = await get_user_config(data.get('_auth'), data.get('_config'))
        if not user_config.get('cavatica_api_key'): raise Exception('Missing CAVATICA API Key')
        if not user_config.get('cavatica_project'): raise Exception('Missing CAVATICA Project')
        cavatica_project = user_config.get('cavatica_project')
      data['_storage'] = f"cavatica://{cavatica_project}"
    else:
      assert data['_storage'].startsWith('cavatica://'), 'CAVATICA executor requires CAVATICA storage'
  #
  return data
