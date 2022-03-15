import os
import io
import random
import asyncio
import fsspec
import json
import logging

from appyter.parse.nb import nb_from_ipynb_io
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.dict import dict_merge
from appyter.ext.urllib import join_slash, join_url

class WESExecutor(AbstractExecutor):
  ''' Run executions via a workflow execution service endpoint
  '''
  protocol = 'wes'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    with fsspec.open(self.executor_options['cwl'], 'r') as fr:
      self.cwl = json.loads(fr.read())

  async def submit(self, job):
    async def _submit():
      import aiohttp
      logger.info(f"Submitting execution via WES")
      # NOTE: This is redundant, since the notebook was already created
      #       but is necessary if we want to use the standard `cwl-runner`
      # grab original inputs from notebook
      with fsspec.open(join_url(job['cwd'], job['ipynb']), 'r') as fr:
        nb = nb_from_ipynb_io(fr)
      inputs = nb.metadata['appyter']['nbconstruct']['data']
      # TODO: process inputs
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
      logger.debug(f"{execution=}")
      async with aiohttp.ClientSession(
        headers=dict(
          **self.executor_options.get('headers', {}),
        )
      ) as client:
        data = aiohttp.FormData()
        for filename, bytesio in execution.pop('workflow_attachment'):
          data.add_field('workflow_attachment', bytesio, filename=filename)
        for k, v in execution.items():
          if type(v) in {dict, list}:
            data.add_field(k, json.dumps(v), content_type='application/json')
          else:
            data.add_field(k, v)
        async with client.post(
          join_slash(self.url, '/runs'),
          data=data,
        ) as req:
          res = await req.json()
          logger.debug(f"{res=}")
          return res['run_id']
    return await async_try_n_times(3, _submit)

  async def wait_for(self, run_id):
    import aiohttp
    async with aiohttp.ClientSession(
      headers=dict(
        {'Content-Type': 'application/json'},
        **self.executor_options.get('headers', {}),
      )
    ) as client:
      while True:
        await asyncio.sleep(30 * (0.5 + random.random()))
        logger.debug(f"Checking status of job {run_id=}")
        async with client.get(join_slash(self.url, run_id, 'status')) as req:
          res = await req.json()
          state = res['state']
        logger.debug(f"{state=}")
        #
        if state == 'COMPLETE':
          return 0
        elif state == 'CANCELED':
          return 1
        elif state == 'EXECUTOR_ERROR':
          return -1
