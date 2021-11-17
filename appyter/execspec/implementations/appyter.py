from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.dict import dict_merge

class AppyterExecutor(AbstractExecutor):
  ''' Submit executions to be run by an appyter orchestrator

  This executor only supports submit and not wait_for/run
   as it submits jobs to a queue which manages the execution.
  '''
  protocol = 'appyter'

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
          self.url,
          json=dict_merge(
            self.executor_options.get('params',{}),
            **job,
          ),
        ) as resp:
          queue_size = await resp.json()
          return job['id']
    return await async_try_n_times(3, _submit)
