import logging
logger = logging.getLogger(__name__)

import json
import aiohttp
from pathlib import Path
from fsspec.asyn import AsyncFileSystem
from appyter.ext.fsspec.spec.sync_async import SyncAsyncFileSystem
from appyter.ext.fsspec.spec.mountable import MountableAbstractFileSystem
from appyter.ext.asyncio.helpers import ensure_sync
from appyter.ext.urllib import join_slash
from fsspec.spec import AbstractBufferedFile

class SBFSFileSystem(MountableAbstractFileSystem, SyncAsyncFileSystem, AsyncFileSystem):
  CHUNK_SIZE = 8192

  def __init__(self, *args,
    api_endpoint='https://cavatica-api.sbgenomics.com',
    drs_endpoint='drs://cavatica-ga4gh-api.sbgenomics.com',
    auth_token=None,
    **storage_options,
  ):
    assert auth_token is not None, 'SBFS auth_token is required'
    super().__init__(*args,
      api_endpoint=api_endpoint,
      drs_endpoint=drs_endpoint,
      auth_token=auth_token,
      **storage_options,
    )
    self.auth_token = auth_token
    self.drs_endpoint = drs_endpoint
    self.api_endpoint = api_endpoint

  async def __aenter__(self):
    self._session_mgr = aiohttp.ClientSession(
      headers={
        'X-SBG-Auth-Token': self.auth_token,
      },
      raise_for_status=True,
    )
    self._session = await self._session_mgr.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self._session_mgr.__aexit__(exc_type, exc_value, traceback)

  async def _mkdir(self, path, create_parents=True, exist_ok=True, **kwargs):
    try:
      path_info = await self._info(path)
      if path_info['type'] == 'directory' and exist_ok:
        return path_info
      else:
        raise FileExistsError
    except FileNotFoundError:
      pass
    path_split = path.split('/')
    if len(path_split) <= 2: raise PermissionError
    if len(path_split) == 3:
      user, project, directory = path_split
      async with self._session.post(f"{self.api_endpoint}/v2/files", json=dict(
        project=f"{user}/{project}",
        name=directory,
        type='folder',
      ), raise_for_status=False) as req:
        if req.status == 404:
          raise NotADirectoryError
        else:
          req.raise_for_status()
        res = await req.json()
      return {
        '_id': res['id'],
        'name': f"{user}/{project}/{res['name']}",
        'type': 'directory',
      }
    else:
      parent_directory_path = '/'.join(path_split[:-1])
      directory = path_split[-1]
      try:
        parent_info = await self._info(parent_directory_path)
      except FileNotFoundError:
        if not create_parents:
          raise
        parent_info = await self._mkdir(parent_directory_path, create_parents=True, exist_ok=True)
      
      async with self._session.post(f"{self.api_endpoint}/v2/files", json=dict(
        parent=parent_info['_id'],
        name=directory,
        type='folder',
      )) as req:
        res = await req.json()
      return {
        '_id': res['id'],
        'name': f"{parent_directory_path}/{res['name']}",
        'type': 'directory',
      }

  async def _makedirs(self, path, exist_ok=False, **kwargs):
    return await self._mkdir(path, create_parents=True, exist_ok=exist_ok, **kwargs)

  async def _sbg_rm_file(self, file_id):
    async with self._session.delete(f"{self.api_endpoint}/v2/files/{file_id}", headers={
      'Content-Type': 'application/json',
    }) as res:
      return await res.text()

  async def _rmdir(self, path):
    info = await self._info(path)
    if info['type'] != 'directory': raise NotADirectoryError
    await self._sbg_rm_file(info['_id'])

  async def _rm_file(self, path):
    info = await self._info(path)
    if info['type'] == 'directory': raise IsADirectoryError
    await self._sbg_rm_file(info['_id'])

  async def _rm(self, path, recursive=False, **kargs):
    info = await self._info(path)
    if info['type'] == 'file':
      await self._sbg_rm_file(info['_id'])
    elif info['type'] == 'directory':
      if recursive:
        for child in await self._ls(info['name'], detail=False):
          await self._rm(child)
      await self._sbg_rm_file(info['_id'])
    else:
      raise NotImplementedError

  async def _mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    path1_info = await self._info(path1)
    path2_split = path2.split('/')
    if len(path2_split) <= 2: raise PermissionError
    project2 = '/'.join(path2_split[:2])
    if path1.startswith(project2): # moves only allowed within the same project
      try:
        path2_info = await self._info(path2)
        # overwrite/merge
        if path2_info['type'] == 'file':
          await self._rm_file(path2)
      except FileNotFoundError:
        # new file/directory
        if path1_info['type'] == 'directory':
          await self._mkdir(path2)
      #
      if path1_info['type'] == 'directory':
        if not recursive: raise IsADirectoryError
        for subpath1 in (await self._ls(path1, detail=False)):
          subpath2 = join_slash(path2, subpath1[len(path1):])
          await self._mv(subpath1, subpath2, recursive=recursive, maxdepth=(maxdepth-1) if maxdepth is not None else maxdepth, **kwargs)
        await self._rmdir(path1)
      elif path1_info['type'] == 'file':
        if await self._exists(path2):
          await self._rm_file(path2)
        if len(path2_split) == 3:
          async with self._session.post(f"{self.api_endpoint}/v2/files/{path1_info['_id']}/actions/move", json=dict(
            project=project2,
            name=path2_split[-1],
          )) as res:
            return await res.json()
        else:
          path2_parent_info = await self._info('/'.join(path2_split[:-1]))
          if path2_parent_info['type'] != 'directory': raise NotADirectoryError
          async with self._session.post(f"{self.api_endpoint}/v2/files/{path1_info['_id']}/actions/move", json=dict(
            parent=path2_parent_info['_id'],
            name=path2_split[-1],
          )) as res:
            return await res.json()
      else:
        raise NotImplementedError
    else:
      await self._cp_file(path1, path2, recursive=recursive, maxdepth=maxdepth)
      await self._rm(path1, recursive=recursive)

  async def _cp_file(self, path1, path2, **kwargs):
    path1_info = await self._info(path1)
    path2_split = path2.split('/', maxsplit=2)
    project2 = '/'.join(path2_split[:2])
    if len(path2_split) == 3:
      async with self._session.post(f"{self.api_endpoint}/v2/files/{path1_info['_id']}/actions/copy", json=dict(
        project=project2,
        name=path2_split[-1],
      )) as res:
        return await res.json()
    else:
      path2_parent_info = await self._info('/'.join(path2_split[:-1]))
      if path2_parent_info['type'] != 'directory': raise NotADirectoryError
      async with self._session.post(f"{self.api_endpoint}/v2/files/{path1_info['_id']}/actions/copy", json=dict(
        parent=path2_parent_info['_id'],
        name=path2_split[-1],
      )) as res:
        return await res.json()

  async def _download_info(self, file_info):
    async with self._session.get(f"{self.api_endpoint}/v2/files/{file_info['_id']}/download_info") as req:
      return await req.json()
  
  async def _cat_file(self, path, start=None, end=None, **kwargs):
    file_info = await self._info(path)
    download_info = await self._download_info(file_info)
    if end is None: end = file_info['size']
    elif end > file_info['size']: end = file_info['size']
    elif end < 0: raise Exception('Invalid end')
    if start is None: start = 0
    elif start >= end: return b''
    elif start < 0: raise Exception('Invalid start')
    async with self._session.get(download_info['url'], headers={
      'Range': f"bytes={start}-{end}"
    }) as req:
      return await req.read()

  async def _put_file(self, lpath, rpath, **kwargs):
    lpath = Path(lpath)
    lpath_stat = lpath.stat()
    rpath_split = rpath.split('/')
    if len(rpath_split) == 3:
      rpath_info = dict(
        project='/'.join(rpath_split[:2]),
        name=rpath_split[-1],
        size=lpath_stat.st_size,
        part_size=min(1073741824, lpath_stat.st_size),
      )
    elif len(rpath_split) > 3:
      parent_info = await self._info('/'.join(rpath_split[:-1]))
      rpath_info = dict(
        parent=parent_info['_id'],
        name=rpath_split[-1],
        size=lpath_stat.st_size,
        part_size=min(1073741824, lpath_stat.st_size),
      )
    else:
      raise PermissionError
    # initiate multipart upload
    logger.debug(f"Initiating multipart upload for {rpath}: {rpath_info}")
    async with self._session.post(f"{self.api_endpoint}/v2/upload/multipart", params=dict(overwrite='true'), json=rpath_info) as req:
      upload_info = await req.json()
    try:
      with lpath.open('rb') as fr:
        # for each chunk of size upload_info['part_size']
        for i in range((lpath_stat.st_size // upload_info['part_size']) + 1 if lpath_stat.st_size % upload_info['part_size'] else 0):
          # get part_info
          logger.info(f"Initiating multipart part {i+1} upload for {rpath_info['name']}")
          async with self._session.get(f"{self.api_endpoint}/v2/upload/multipart/{upload_info['upload_id']}/part/{i+1}") as req:
            part_info = await req.json()
          # load buffer with upload_info['part_size']
          buf = fr.read(upload_info['part_size'])
          # upload part
          async with self._session.request(part_info['method'], part_info['url'], data=buf) as req:
            await req.read()
            upload_response = {'headers': {k: json.loads(req.headers.get(k)) for k in part_info['report']['headers']}}
          logger.debug(f"{upload_response=}")
          # report uploaded part
          async with self._session.post(f"{self.api_endpoint}/v2/upload/multipart/{upload_info['upload_id']}/part", json=dict(
            part_number=i+1,
            response=upload_response,
          )) as req:
            await req.read()
      # report multipart completion
      async with self._session.post(f"{self.api_endpoint}/v2/upload/multipart/{upload_info['upload_id']}/complete", headers={
        'Content-Type': 'application/json',
      }) as req:
        await req.read()
    except:
      # abort multipart upload
      async with self._session.delete(f"{self.api_endpoint}/v2/upload/multipart/{upload_info['upload_id']}", headers={
        'Content-Type': 'application/json',
      }) as req:
        await req.read()
      raise
    logger.debug(f"Multipart upload for {rpath} completed")

  async def _get_file(self, rpath, lpath, **kwargs):
    file_info = await self._info(rpath)
    download_info = await self._download_info(file_info)
    lpath = Path(lpath)
    async with self._session.get(download_info['url']) as req:
      with lpath.open('wb') as fw:
        async for data in req.content.iter_chunked(SBFSFileSystem.CHUNK_SIZE):
          fw.write(data)

  async def _get_drs(self, path, **kwargs):
    file_info = await self._info(path, **kwargs)
    return f"{self.drs_endpoint}/{file_info['_id']}"

  def get_drs(self, path, **kwargs):
    return ensure_sync(self._get_drs(path, **kwargs))

  async def _info(self, path, **kwargs):
    path_split = [] if path in {'', '.', '/', './'} else path.split('/')
    if len(path_split) == 0:
      return {'name': path, 'type': 'directory'}
    elif len(path_split) == 1:
      project_user, = path_split
      async with self._session.get(f"{self.api_endpoint}/v2/projects/{project_user}") as req:
        projects = await req.json()
      if len(projects['items']) == 0:
        raise FileNotFoundError(path)
      elif len(projects['items']) > 1:
        raise Exception('Ambiguity')
      return {'name': project_user, 'type': 'directory'}
    elif len(path_split) == 2:
      project_user, proj_id = path_split
      async with self._session.get(f"{self.api_endpoint}/v2/projects/{project_user}", params=dict(
        name=proj_id
      ), raise_for_status=False) as req:
        if req.status == 404:
          raise FileNotFoundError(path)
        else:
          req.raise_for_status()
        projects = await req.json()
      if len(projects['items']) == 0:
        raise FileNotFoundError(path)
      elif len(projects['items']) == 2:
        raise Exception('Ambiguity')
      else:
        return {'name': f"{project_user}/{proj_id}", 'type': 'directory'}
    elif len(path_split) == 3:
      acc, proj_id, name = path_split
      proj = acc + '/' + proj_id
      async with self._session.get(f"{self.api_endpoint}/v2/files", params=dict(
        project=proj, name=name,
      ), raise_for_status=False) as req:
        if req.status == 404:
          raise FileNotFoundError(path)
        else:
          req.raise_for_status()
        items = await req.json()
      if len(items['items']) == 0:
        raise FileNotFoundError(path)
      elif len(items['items']) > 1:
        raise Exception('Ambiguity error')
      item = items['items'][0]
      item_name = f"{proj}/{item['name']}"
      if item['type'] == 'file':
        async with self._session.get(f"{self.api_endpoint}/v2/files/{item['id']}", params=dict(
          fields='size',
        )) as req:
          item_details = await req.json()
        return {
          '_id': item['id'],
          'name': item_name,
          'type': 'file',
          'size': item_details['size'],
        }
      elif item['type'] == 'folder':
        return {
          '_id': item['id'],
          'name': item_name,
          'type': 'directory',
        }
      else:
        raise NotImplementedError
    elif len(path_split) > 3:
      item_directory = '/'.join(path_split[:-1])
      parent_info = await self._info(item_directory)
      name = path_split[-1]
      async with self._session.get(f"{self.api_endpoint}/v2/files", params=dict(
        parent=parent_info['_id'], name=name,
      ), raise_for_status=False) as req:
        if req.status == 404:
          raise FileNotFoundError(path)
        else:
          req.raise_for_status()
        items = await req.json()
      if len(items['items']) == 0:
        raise FileNotFoundError(path)
      elif len(items['items']) > 1:
        raise Exception('Ambiguity error')
      item = items['items'][0]
      item_name = f"{item_directory}/{item['name']}"
      if item['type'] == 'file':
        async with self._session.get(f"{self.api_endpoint}/v2/files/{item['id']}", params=dict(
          fields='size',
        )) as req:
          item_details = await req.json()
        return {
          '_id': item['id'],
          'name': item_name,
          'type': 'file',
          'size': item_details['size'],
        }
      elif item['type'] == 'folder':
        return {
          '_id': item['id'],
          'name': item_name,
          'type': 'directory',
        }
      else:
        raise NotImplementedError

  async def _ls(self, path, detail=True, **kwargs):
    path_split = [] if path in {'', '.', '/', './'} else path.split('/')
    results = {}
    if len(path_split) == 0:
      async with self._session.get(f"{self.api_endpoint}/v2/projects") as req:
        projects = await req.json()
      for proj in projects['items']:
        proj_id_split = proj['id'].split('/')
        acc, _ = proj_id_split
        results[acc] = {'name': acc, 'type': 'directory'} if detail else acc
    elif len(path_split) == 1:
      project_user, = path_split
      async with self._session.get(f"{self.api_endpoint}/v2/projects/{project_user}") as req:
        projects = await req.json()
      for proj in projects['items']:
        proj_id_split = proj['id'].split('/')
        if path_split[0] == proj_id_split[0]:
          results[proj['id']] = {'name': proj['id'], 'type': 'directory'} if detail else proj['id']
    elif len(path_split) == 2:
      acc, proj_id = path_split
      proj = f"{acc}/{proj_id}"
      async with self._session.get(f"{self.api_endpoint}/v2/files", params=dict(
        project=proj,
      ), raise_for_status=False) as req:
        if req.status == 404:
          raise FileNotFoundError(path)
        else:
          req.raise_for_status()
        items = await req.json()
      for item in items['items']:
        item_name = proj + '/' + item['name']
        if detail:
          if item['type'] == 'file':
            async with self._session.get(f"{self.api_endpoint}/v2/files/{item['id']}", params=dict(
              fields='size',
            )) as req:
              file_details = await req.json()
            results[item_name] = {
              '_id': item['id'],
              'name': item_name,
              'type': 'file',
              'size': file_details['size'],
            }
          elif item['type'] == 'folder':
            results[item_name] = {
              '_id': item['id'],
              'name': item_name,
              'type': 'directory',
            }
          else:
            raise NotImplementedError
        else:
          results[item_name] = item_name
    elif len(path_split) > 2:
      path_info = await self._info(path)
      if path_info['type'] == 'directory':
        async with self._session.get(f"{self.api_endpoint}/v2/files", params=dict(
          parent=path_info['_id'],
        )) as req:
          items = await req.json()
        for item in items['items']:
          item_name = path_info['name'] + '/' + item['name']
          if detail:
            if item['type'] == 'file':
              async with self._session.get(f"{self.api_endpoint}/v2/files/{item['id']}", params=dict(
                fields='size',
              )) as req:
                file_details = await req.json()
              results[item_name] = {
                '_id': item['id'],
                'name': item_name,
                'type': 'file',
                'size': file_details['size'],
              }
            elif item['type'] == 'folder':
              results[item_name] = {
                '_id': item['id'],
                'name': item_name,
                'type': 'directory',
              }
            else:
              raise NotImplementedError
          else:
            results[item_name] = item_name
      else:
        return [path_info] if detail else [path_info['name']]
    return list(results.values())

  def _open(self, path, mode="rb", block_size=None, cache_options=None, **kwargs):
    ''' Implements certain write ops, to use `open` with mode='w' or mode='a' use writecache,
    i.e. writecache::chroot::sbfs://*
    '''
    if mode != "rb":
      raise NotImplementedError
    return SBFSBufferedFile(self, path, mode=mode, block_size=block_size, cache_options=cache_options, **kwargs)

class SBFSBufferedFile(AbstractBufferedFile):
  def __init__(self, fs, path, mode="rb", **kwargs):
      super().__init__(fs, path, mode=mode, **kwargs)

  def _fetch_range(self, start, end):
    return self.fs.cat_file(self.path, start=start, end=end)
