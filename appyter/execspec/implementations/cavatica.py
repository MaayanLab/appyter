import sys
import shutil
import logging
logger = logging.getLogger(__name__)
from appyter.execspec.implementations.wes import WESExecutor
from appyter.ext.fsspec.core import url_to_fs_ex
from appyter.ext.fsspec.sbfs import SBFSFileSystem
from appyter.ext.fsspec.chroot import ChrootFileSystem
from appyter.ext.fsspec.writecache import WriteCacheFileSystem
from appyter.ext.urllib import join_url, url_filename
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
        fo=join_url(self.executor_options['project'], 'appyter'),
      ),
    )
    await ensure_async(self.fs.__enter__)()
    return await super().__aenter__()

  async def __aexit__(self, type, value, traceback):
    await ensure_async(self.fs.__exit__)(type, value, traceback)
    return await super().__aexit__(type, value, traceback)

  async def _prepare(self, job):
    wes_job = await super()._prepare(job)
    base_path = join_url('output', job['session'])
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
          uri_parsed = parse_file_uri(v['path'])
          filename = uri_parsed.fragment or url_filename(v['path'])
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
              fw = await ensure_async(self.fs.open)(join_url(base_path, filename), 'wb')
              await ensure_async(shutil.copyfileobj)(fr, fw)
              await ensure_async(fw.close)()
              await ensure_async(fr.close)()
              drs_uri = await ensure_async(self.fs.get_drs)(join_url(base_path, filename))
          except:
            if getattr(fs, '__exit__', None) is not None: fs.__exit__(sys.exc_info())
            raise
          else:
            if getattr(fs, '__exit__', None) is not None: fs.__exit__(None, None, None)
          # use the drs uri
          logger.getChild(k).debug(f"{drs_uri=}")
          v['path'] = drs_uri
    return wes_job
