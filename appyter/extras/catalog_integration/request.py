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
  return data
