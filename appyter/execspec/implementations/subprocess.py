import os
import sys
import json
import asyncio
from appyter.execspec.spec import AbstractExecutor

class SubprocessExecutor(AbstractExecutor):
  ''' Run executions in a subprocess
  '''
  protocol = 'subprocess'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    self._procs = {}

  async def submit(self, job):
    self._procs[job['id']] = await asyncio.create_subprocess_exec(
      sys.executable, '-u', '-m',
      'appyter', 'orchestration', 'job', json.dumps(job),
      stdout=sys.stdout,
      stderr=sys.stderr,
      env=dict(
        PYTHONPATH=':'.join(sys.path),
        PATH=os.environ['PATH'],
      ),
    )
    return job['id']

  async def wait_for(self, run_id):
    return await (self._procs.pop(run_id)).wait()
