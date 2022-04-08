import re
import aiohttp
import fsspec
from fsspec.asyn import AsyncFileSystem
from appyter.ext.fsspec.spec.sync_async import SyncAsyncFileSystem
from appyter.ext.yarl import URLEx
from appyter.ext.urllib import join_url

drs_matcher = re.compile(r'^drs://([^/]+)/(.+)$', re.IGNORECASE)

class DRSFileSystem(SyncAsyncFileSystem, AsyncFileSystem):
  protocol = 'drs'

  def __init__(self, *args):
    super().__init__()

  @classmethod
  def _strip_protocol(cls, path):
    """For DRS, we always want to keep the full URL"""
    return path

  @classmethod
  def _parent(cls, path):
    # override, since _strip_protocol is different for URLs
    par = super()._parent(path)
    if len(par) > 6:  # "drs://..."
        return par
    return ""

  async def __aenter__(self):
    self._session_mgr = aiohttp.ClientSession()
    self._session = await self._session_mgr.__aenter__()
    return self

  async def __aexit__(self, exc_type, exc_value, traceback):
    await self._session_mgr.__aexit__(exc_type, exc_value, traceback)

  async def _info(self, path, **kwargs):
    ''' Use DRS To find info about the object
    _id contains the DRS ID
    _url contains an fsspec compatible url
    '''
    # lookup DRS object
    async with self._session.get(drs_matcher.sub('https://$1/ga4gh/drs/v1/objects/$2', path)) as req:
      if req.status != 200:
        raise FileNotFoundError
      info = await req.json()
    # obtain first compatible access method
    acceptible_types = {'s3', 'gs', 'ftp', 'https'}
    access_method = None
    for access_method in info.get('access_methods', []):
      if access_method['type'] in acceptible_types:
        break
    if access_method is None: raise RuntimeError('Invalid DRS Implementation')
    elif access_method['type'] not in acceptible_types: raise NotImplementedError
    # obtain access url
    if access_method.get('access_url'):
      access_url = access_method['access_url']
    elif access_method.get('access_id'):
      async with self._session.get(join_url(
        drs_matcher.sub('https://$1/ga4gh/drs/v1/objects/$2/access/', path),
        access_method['access_id'],
      )) as req:
        if req.status != 200:
          raise RuntimeError('Invalid DRS Implementation')
        access_url = await req.json()
    else:
      raise RuntimeError('Invalid DRS Implementation')
    # convert access_url into fsspec url
    url = URLEx(access_url['url']).with_fragment(None)
    if access_url.get('headers'):
      url = url.with_fragment_query(access_url.get('headers', {}))
    if access_method.get('region'):
      url = url.update_fragment_query({
        f"{access_method['type']}.region": access_method['region']
      })
    #
    return {
      '_id': info['id'],
      '_url': str(url),
      'type': 'file',
      'name': path,
      'size': info['size'],
    }

  async def _ls(self, path, **kwargs):
    raise NotImplementedError

  def _open(self, path, mode="rb", **kwargs):
    ''' Open the path with the url prepared during `_info`
    '''
    if mode != "rb": raise NotImplementedError
    path_info = self.info(path)
    return fsspec.open(path_info['_url'], mode=mode, **kwargs)