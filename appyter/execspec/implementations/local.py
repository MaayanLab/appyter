import asyncio
from appyter.execspec.spec import AbstractExecutor

class LocalExecutor(AbstractExecutor):
  ''' Run executions with the same process
  
  Not ideal in most circumstances:
  - it can leak errors to the notebook
  - internal state can get messed with
  '''
  protocol = 'local'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    self._tasks = {}

  async def submit(self, job):
    from appyter.orchestration.job.job import execute_async
    self._tasks[job['id']] = asyncio.create_task(execute_async(job))
    return job['id']

  async def wait_for(self, run_id):
    return await self._tasks.pop(run_id)
