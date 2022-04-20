from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.try_n_times import async_try_n_times
from appyter.ext.dict import dict_merge

class DispatchExecutor(AbstractExecutor):
  ''' Submit executions to be run by an appyter orchestration dispatcher

  This executor only supports submit and not wait_for/run
   as it submits jobs to a queue which manages the execution.
  
  usage:
  dispatch::http://appyter-orchestrator:5000?params.executor=docker::maayanlab/appyter-example:latest
  '''
  protocol = 'dispatch'

  async def __aenter__(self):
    import aiohttp
    self.session = aiohttp.ClientSession(
      headers=dict(
        {'Content-Type': 'application/json'},
        **self.executor_options.get('headers', {}),
      )
    )
    self.client = await self.session.__aenter__()
    return await super().__aenter__()
  
  async def __aexit__(self, type, value, traceback):
    await self.session.__aexit__(type, value, traceback)
    await super().__aexit__(type, value, traceback)

  async def _submit(self, job):
    async with self.client.post(
      self.url,
      json=dict_merge(
        self.executor_options.get('params',{}),
        **dict(job, storage=job['storage']),
      ),
    ) as resp:
      queue_size = await resp.json()
      return queue_size

  async def _run(self, **job):
    yield dict(type='status', data=f"Submitting appyter for execution..")
    queue_size = await async_try_n_times(3, self._submit, job)
    yield dict(type='status', data=f"Queued successfully, you are at position {queue_size}, your execution will begin when resources are available..")
    # TODO: room drop hotfix until we have queue tracking
    import asyncio
    await asyncio.sleep(60)
