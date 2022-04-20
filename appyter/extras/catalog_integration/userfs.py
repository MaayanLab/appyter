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
  ''' Convert all `user://` file_uris into `drs://` or `storage://` uris
  '''
  # TODO: this is a hack for now,
  #  the whole thing should probably be part of the file field
  files = {
    k[len('_file:'):]: v
    for k, v in data.items()
    if k.startswith('_file:')
  }
  if any(
    file_uri.startswith('user://')
    for file_uri in files.values()
  ):
    from appyter.ext.dict import dict_typed_flatten, dict_typed_unflatten
    flat_data = dict_typed_flatten(data)
    async with ensure_async_contextmanager(await create_userfs(data)) as userfs:
      async with ensure_async_contextmanager(url_to_chroot_fs(str(URI(storage).join('input')))) as storagefs:
        for filename, file_uri in files.items():
          if file_uri.startswith('user://'):
            existing_file_uri = str(URI(file_uri).with_fragment_path(filename))
            try:
              # Use DRS if it's available
              new_file_uri_without_filename = await ensure_async(userfs.get_drs)(file_uri[len('user://'):])
              new_file_uri = str(URI(new_file_uri_without_filename).with_fragment_path(filename))
            except:
              # Otherwise put it into `storage://`
              new_file_uri = await ensure_async(organize_file_content)(storagefs, userfs, file_uri[len('user://'):], filename=filename)
              new_file_uri_without_filename = str(URI(new_file_uri).with_fragment_path(None))
            # replace the uri if it appears in `data`
            flat_data = [
              (K, new_file_uri_without_filename) if K[-1] == f"_file:{filename}" else (K, new_file_uri if v == existing_file_uri else v)
              for K, v in flat_data
            ]
    return dict_typed_unflatten(flat_data)
  return data
