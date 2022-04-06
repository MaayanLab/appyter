import re

from appyter.extras.catalog_integration.user_config import get_user_config

async def prepare_storage(data):
  ''' Safely translate public facing storage URIs into internally operable fsspec URIs
  '''
  if data.get('_storage'):
    # cavatica storage provider, obtain CAVATICA API Key and instantiate sbfs
    m = re.match(r'^cavatica://(?P<user>[a-z0-9_-]+)/(?P<project>[a-z0-9_-]+)$', data['_storage'])
    if m:
      user_config = await get_user_config(data.get('_auth'), data.get('_config'))
      if not user_config.get('cavatica_api_key'): raise PermissionError
      assert re.match(r'^[0-9a-f]+$', user_config['cavatica_api_key']) is not None, 'Malformed CAVATICA API Key'
      return f"writecache::chroot::sbfs://{m.group('user')}/{m.group('project')}/appyter/#?sbfs.auth_token={user_config['cavatica_api_key']}"
    else:
      raise Exception('Unrecognized storage URI')
