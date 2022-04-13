from appyter.ext.asyncio.helpers import ensure_async, ensure_async_contextmanager
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.urllib import URI
from appyter.extras.catalog_integration.uploads import list_files
from appyter.extras.catalog_integration.user_config import get_user_config
from appyter.render.flask_app.upload import organize_file_content

async def create_userfs(data):
  from appyter.ext.fsspec.mapperfs import MapperFileSystem
  pathmap = {}
  user_config = await get_user_config(data['_auth'], data['_config'])
  try:
    files = await list_files(data['_auth'], data['_config'])
    pathmap.update({
      f"uploads/{file['filename']}": file['file']['id']
      for file in files
    })
  except:
    pass
  try:
    import re
    if not user_config.get('cavatica_api_key'): raise PermissionError
    assert re.match(r'^[0-9a-f]+$', user_config['cavatica_api_key']) is not None, 'Malformed CAVATICA API Key'
    pathmap['integrations/cavatica'] = f"chroot::sbfs://#?sbfs.auth_token={user_config['cavatica_api_key']}"
  except:
    pass
  return MapperFileSystem(pathmap=pathmap)

async def upload_user_to_storage(storage, data):
  ''' Convert all `user://` file_uris into `storage://` uris
  '''
  files = {
    k[len('_file:'):]: v
    for k, v in data.items()
    if k.startswith('_file:')
  }
  if any(
    file_uri.startswith('user://')
    for file_uri in files.values()
  ):
    async with ensure_async_contextmanager(await create_userfs(data)) as userfs:
      async with ensure_async_contextmanager(url_to_chroot_fs(str(URI(storage).join('input')))) as storagefs:
        for filename, file_uri in files.items():
          if file_uri.startswith('user://'):
            data[f"_file:{filename}"] = await ensure_async(organize_file_content)(storagefs, userfs, file_uri[len('user://'):], filename=filename)
  return data
