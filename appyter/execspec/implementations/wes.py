import os
import io
import re
import random
import asyncio
import json
import aiohttp
import logging
import traceback
import functools

from appyter.parse.nb import nb_from_ipynb_io
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.fsspec.util import fsspec_read_and_run
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.dict import dict_filter_none, dict_merge
from appyter.ext.urllib import URI, join_slash

class WESExecutor(AbstractExecutor):
  ''' Run executions via a workflow execution service endpoint
  '''
  protocol = 'wes'

  def __init__(self, url=None, config={}, **kwargs):
    super().__init__(url=re.sub(r'^wes://', 'https://', url), **kwargs)
    self.config = config

  async def __aenter__(self):
    await super().__aenter__()
    from appyter.parse.nb import nb_from_ipynb_io
    self.cwl = await fsspec_read_and_run(self.executor_options['cwl'], lambda fr: json.load(fr))
    self.nbtemplate = await fsspec_read_and_run(join_slash(self.config['CWD'], self.config['IPYNB']), nb_from_ipynb_io)
    self.session = aiohttp.ClientSession(
      headers=dict(
        {'Accept': 'application/json'},
        **self.executor_options.get('headers', {}),
      )
    )
    self.client = await self.session.__aenter__()
    return self
  
  async def __aexit__(self, type, value, traceback):
    await self.session.__aexit__(type, value, traceback)
    await super().__aexit__(type, value, traceback)

  async def _prepare(self, job):
    # NOTE: This is redundant, since the notebook was already created
    #       but is necessary if we want to use the standard `cwl-runner`
    from appyter.context import get_jinja2_env
    from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
    nb = await fsspec_read_and_run(str(URI(job['storage']).join(job['cwd'], job['ipynb'])), nb_from_ipynb_io)
    env = get_jinja2_env(config=self.config, context=nb.metadata['appyter']['nbconstruct']['data'], session=job['session'])
    inputs = dict_filter_none({
      field.args['name']: field.to_cwl_value()
      for field in parse_fields_from_nbtemplate(env, self.nbtemplate, deep=True)
    })
    inputs['s'] = job['url']
    inputs['w'] = f"appyter/output/{job['session']}"
    return dict_merge(
      self.executor_options.get('params', {}),
      workflow_params=dict(inputs=inputs),
      workflow_url='#/workflow_attachment/0',
      workflow_attachment=[
        [
          os.path.basename(self.executor_options['cwl']),
          functools.partial(io.BytesIO, json.dumps(self.cwl).encode()),
        ],
      ],
      workflow_type='CWL',
      workflow_type_version=self.cwl['cwlVersion'],
    )

  async def _submit(self, wes_job):
    data = aiohttp.FormData()
    for k, v in wes_job.items():
      if k == 'workflow_attachment':
        for filename, bytesio in v:
          data.add_field('workflow_attachment', bytesio(), filename=filename)
      elif type(v) in {dict, list}:
        data.add_field(k, json.dumps(v), content_type='application/json')
      else:
        data.add_field(k, v)
    async with self.client.post(
      join_slash(self.url, 'ga4gh/wes/v1', 'runs'),
      data=data,
    ) as req:
      res = await req.json()
      logger.info(f"{res=}")
      return res['run_id']

  async def _watch_state(self, run_id):
    current_state = None
    while True:
      await asyncio.sleep(15 * (0.5 + random.random()))
      logger.debug(f"Checking status of job {run_id=}")
      async with self.client.get(join_slash(self.url, 'ga4gh/wes/v1', 'runs', run_id, 'status')) as req:
        res = await req.json()
        state = res['state']
      logger.debug(f"{state=}")
      if current_state != state:
        current_state = state
        yield current_state

  async def _finalize(self, job, wes_job):
    pass

  async def _run(self, **job):
    yield dict(type='status', data=f"Preparing WES parameters...")
    wes_job = await async_try_n_times(3, self._prepare, job)
    yield dict(type='status', data=f"Dispatching WES execution...")
    logger.info(f"{wes_job=}")
    run_id = await async_try_n_times(3, self._submit, wes_job)
    yield dict(type='status', data=f"Dispatched successfully, your execution will begin soon..")
    async for state in self._watch_state(run_id):
      if state == 'QUEUED':
        yield dict(type='status', data=f"Queued successfully..")
      elif state == 'INITIALIZING':
        yield dict(type='status', data=f"Computational resources are being initialized..")
      elif state == 'RUNNING':
        yield dict(type='status', data=f"Task is now running..")
      elif state == 'CANCELING':
        yield dict(type='error', data=f"Task is being cancelled!")
        break
      elif state == 'CANCELED':
        yield dict(type='error', data=f"Task was cancelled!")
        break
      elif state == 'EXECUTOR_ERROR':
        yield dict(type='error', data=f"Task had an error and did not complete successfully!")
        break
      elif state == 'COMPLETE':
        break
      else:
        yield dict(type='error', data=f"An unknown state reported by WES")
        logger.warning(f"Unhandled state received: {state}")
        break
    #
    try:
      await self._finalize(job, wes_job)
    except:
      logger.error(traceback.print_exc())
      yield dict(type='error', data=f"Task failed to finalize")
    else:
      yield dict(type='status', data=f"Task completed")
