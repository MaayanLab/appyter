import re
from appyter.ext.flask import request_get
from appyter.ext.dict import dict_filter_none

def prepare_data(req):
  ''' Extract additional fields from request
  '''
  data = dict_filter_none({
    k: request_get(req, k)
    for k in [
      '_auth',
      '_executor',
      '_storage',
    ]
  })
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
      from appyter.ext.asyncio.helpers import ensure_sync
      from appyter.extras.catalog_integration.user_config import get_user_config
      user_config = ensure_sync(get_user_config(data['_auth']))
      if not user_config.get('cavatica_api_key'): raise Exception('Missing CAVATICA API Key')
      if not user_config.get('cavatica_project'): raise Exception('Missing CAVATICA Project')
      data['_storage'] = f"cavatica://{user_config.get('cavatica_project')}"
    else:
      assert data['_storage'].startsWith('cavatica://'), 'CAVATICA executor requires CAVATICA storage'
  #
  return data
