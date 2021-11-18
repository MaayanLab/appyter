import random
import asyncio
import fsspec
import logging
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.dict import dict_merge
from appyter.ext.urllib import join_slash

class WESExecutor(AbstractExecutor):
  ''' Run executions via a workflow execution service endpoint
  '''
  protocol = 'wes'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    with fsspec.open(self.executor_options['cwl'], 'r') as fr:
      self.cwl = fr.read()

  async def submit(self, job):
    async def _submit():
      import aiohttp
      async with aiohttp.ClientSession(
        headers=dict(
          {'Content-Type': 'application/json'},
          **self.executor_options.get('headers', {}),
        )
      ) as client:
        async with client.post(
          join_slash(self.url, '/runs'),
          json=dict_merge(
            self.executor_options.get('params', {}),
            workflow_params=dict(
              inputs=job,
            ),
            # TODO: possibly create on the fly
            workflow_url='#/workflow_attachment/0',
            workflow_attachment=[self.cwl],
          ),
        ) as req:
          res = await req.json()
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
