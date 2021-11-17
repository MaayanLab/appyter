import random
import asyncio
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
            workflow_url='#/workflow_attachment/0', #TODO: possibly store this ahead of time via sbfs
            workflow_attachment=[
              # TODO: create CWL & insert here
            ],
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
