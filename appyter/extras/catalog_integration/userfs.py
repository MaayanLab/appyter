from appyter.extras.catalog_integration.uploads import list_files
from appyter.extras.catalog_integration.user_config import get_user_config

async def create_userfs(data):
  from appyter.ext.fsspec.mapperfs import MapperFileSystem
  pathmap = {}
  user_config = await get_user_config(data['_auth'], data['_config'])
  try:
    import re
    if not user_config.get('cavatica_api_key'): raise PermissionError
    assert re.match(r'^[0-9a-f]+$', user_config['cavatica_api_key']) is not None, 'Malformed CAVATICA API Key'
    pathmap['integrations/cavatica'] = f"chroot::sbfs://#?sbfs.auth_token={user_config['cavatica_api_key']}"
  except:
    pass
  return MapperFileSystem(pathmap=pathmap)
