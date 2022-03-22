import sys
import json
import shutil
import logging
logger = logging.getLogger(__name__)
from appyter.execspec.implementations.wes import WESExecutor
from appyter.ext.fsspec.core import url_to_fs_ex
from appyter.ext.fsspec.sbfs import SBFSFileSystem
from appyter.ext.fsspec.chroot import ChrootFileSystem
from appyter.ext.fsspec.writecache import WriteCacheFileSystem
from appyter.ext.urllib import join_slash, url_filename
from appyter.ext.asyncio.helpers import ensure_async
from appyter.ext.urllib import parse_file_uri


class CavaticaExecutor(WESExecutor):
  ''' Run executions in CAVATICA
  cavatica#?project=myuser/myproject&auth_token=MYKEY&cwl=example.cwl
  '''
  protocol = 'cavatica'

  def __init__(self,
    url=None,
    project=None,
    auth_token=None,
    api_endpoint='https://cavatica-api.sbgenomics.com/',
    wes_endpoint='https://cavatica-ga4gh-api.sbgenomics.com/ga4gh/wes/',
    drs_endpoint='drs://cavatica-ga4gh-api.sbgenomics.com',
    params={},
    headers={},
    **kwargs,
  ):
    assert project, 'CAVATICA Project required'
    assert auth_token, 'CAVATICA API Key required'
    super().__init__(
      url=wes_endpoint,
      api_endpoint=api_endpoint,
      drs_endpoint=drs_endpoint,
      project=project,
      auth_token=auth_token,
      params=dict(params, workflow_params=dict(params.get('workflow_params', {}), project=project)),
      headers=dict(headers, **{ 'X-SBG-Auth-Token': auth_token }),
      **kwargs,
    )

  async def __aenter__(self):
    self.fs = WriteCacheFileSystem(
      fs=ChrootFileSystem(
        fs=SBFSFileSystem(
          auth_token=self.executor_options['auth_token'],
          api_endpoint='https://cavatica-api.sbgenomics.com',
          drs_endpoint='drs://cavatica-ga4gh-api.sbgenomics.com',
        ),
        fo=join_slash(self.executor_options['project'], 'appyter'),
      ),
    )
    await ensure_async(self.fs.__enter__)()
    # WES establishes an authenticated client session
    await super().__aenter__()
    # augment CWL for CAVATICA -- namely, the revision must be specified
    #  we'll use cavatica's app API to determine which revision is necessary
    async with self.session.get(
      join_slash(self.executor_options['api_endpoint'], 'v2', 'apps', self.executor_options['project'], self.cwl['id'])
    ) as req:
      if req.status == 404:
        self.cwl['id'] = f"{self.cwl['id']}/0"
      else:
        res = await req.json()
        if json.dumps(res['raw']['hints'], sort_keys=True) == json.dumps(self.cwl['hints'], sort_keys=True):
          self.cwl['id'] = f"{self.cwl['id']}/{res['revision']}"
        else:
          self.cwl['id'] = f"{self.cwl['id']}/{res['revision']+1}"
    logger.info(f"{self.cwl['id']=}")
    return self

  async def __aexit__(self, type, value, traceback):
    await ensure_async(self.fs.__exit__)(type, value, traceback)
    return await super().__aexit__(type, value, traceback)

  async def _prepare(self, job):
    wes_job = await super()._prepare(job)
    base_path = join_slash('output', job['session'])
    await ensure_async(self.fs.mkdir)(
      base_path,
      create_parents=True,
      exist_ok=True,
    )
    # TODO: could potentially use CAVATICA's DRS import for this
    for k, v in wes_job['workflow_params']['inputs'].items():
      if type(v) == dict and v.get('class') == 'File':
        if not v['path'].startswith(self.executor_options['drs_endpoint']):
          logger.getChild(k).debug(f"identified file path {v['path']}...")
          filename = v['name']
          fs, fspath = url_to_fs_ex(v['path'])
          if getattr(fs, '__enter__', None) is not None: fs.__enter__()
          try:
            # attempt to use the filesystem's own drs provider
            logger.getChild(k).debug('trying get_drs...')
            try: drs_uri = await ensure_async(fs.get_drs)(fspath)
            except AttributeError: drs_uri = None
            # fall back to copying over to CAVATICA-fs
            if drs_uri is None or not drs_uri.startswith(self.executor_options['drs_endpoint']):
              logger.getChild(k).debug('copying to sbfs...')
              fr = await ensure_async(fs.open)(fspath, 'rb')
              fw = await ensure_async(self.fs.open)(join_slash(base_path, filename), 'wb')
              await ensure_async(shutil.copyfileobj)(fr, fw)
              await ensure_async(fw.close)()
              await ensure_async(fr.close)()
              drs_uri = await ensure_async(self.fs.get_drs)(join_slash(base_path, filename))
          except:
            if getattr(fs, '__exit__', None) is not None: fs.__exit__(sys.exc_info())
            raise
          else:
            if getattr(fs, '__exit__', None) is not None: fs.__exit__(None, None, None)
          # use the drs uri
          logger.getChild(k).debug(f"{drs_uri=}")
          v['path'] = drs_uri
    return wes_job
