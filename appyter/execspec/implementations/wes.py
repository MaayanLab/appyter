import os
import io
import random
import asyncio
import fsspec
import json
import aiohttp
import logging

from appyter.parse.nb import nb_from_ipynb_io
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.dict import dict_merge
from appyter.ext.urllib import join_slash

class WESExecutor(AbstractExecutor):
  ''' Run executions via a workflow execution service endpoint
  '''
  protocol = 'wes'

  def __init__(self, url=None, config={}, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    self.config = config
    with fsspec.open(self.executor_options['cwl'], 'r') as fr:
      self.cwl = json.loads(fr.read())
    from appyter.parse.nb import nb_from_ipynb_io
    with fsspec.open(join_slash(config['CWD'], config['IPYNB']), 'r') as fr:
      self.nbtemplate = nb_from_ipynb_io(fr)

  async def __aenter__(self):
    self.session = aiohttp.ClientSession(
      headers=dict(
        {'Accept': 'application/json'},
        **self.executor_options.get('headers', {}),
      )
    )
    self.client = await self.session.__aenter__()
    return await super().__aenter__()
  
  async def __aexit__(self, type, value, traceback):
    await self.session.__aexit__(type, value, traceback)
    await super().__aexit__(type, value, traceback)

  async def _submit(self, job):
    # NOTE: This is redundant, since the notebook was already created
    #       but is necessary if we want to use the standard `cwl-runner`
    from appyter.context import get_jinja2_env
    from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
    with fsspec.open(join_slash(job['cwd'], job['ipynb']), 'r') as fr:
      nb = nb_from_ipynb_io(fr)
    env = get_jinja2_env(config=self.config, context=nb.metadata['appyter']['nbconstruct']['data'], session=job['session'])
    inputs = {
      field.args['name']: field.to_cwl_value()
      for field in parse_fields_from_nbtemplate(env, self.nbtemplate, deep=True)
    }
    inputs['s'] = job['url']
    # prepare execution params
    execution = dict_merge(
      self.executor_options.get('params', {}),
      workflow_params=dict(inputs=inputs),
      workflow_url='#/workflow_attachment/0',
      workflow_attachment=[
        [
          os.path.basename(self.executor_options['cwl']),
          io.BytesIO(json.dumps(self.cwl).encode()),
        ],
      ],
      workflow_type='CWL',
      workflow_type_version=self.cwl['cwlVersion'],
    )
    logger.info(f"{execution=}")
    data = aiohttp.FormData()
    for filename, bytesio in execution.pop('workflow_attachment'):
      data.add_field('workflow_attachment', bytesio, filename=filename)
    for k, v in execution.items():
      if type(v) in {dict, list}:
        data.add_field(k, json.dumps(v), content_type='application/json')
      else:
        data.add_field(k, v)
    async with self.client.post(
      join_slash(self.url, 'v1', 'runs'),
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
      async with self.client.get(join_slash(self.url, 'v1', 'runs', run_id, 'status')) as req:
        res = await req.json()
        state = res['state']
      logger.debug(f"{state=}")
      if current_state != state:
        current_state = state
        yield current_state

  async def _run(self, **job):
    yield dict(type='status', data=f"Dispatching job using WES")
    run_id = await async_try_n_times(3, self._submit, job)
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
        logger.warn(f"Unhandled state received: {state}")
        yield dict(type='status', data=f"Task completed")
