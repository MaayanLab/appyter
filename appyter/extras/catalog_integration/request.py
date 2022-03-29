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
  if not data.get('_auth') and type(req) != None:
    authorization = req.headers.get('Authorization')
    if authorization:
      m = re.compile(r'^Bearer (.+)$')
      if m: data['_auth'] = m.group(1)
  #
  return data
