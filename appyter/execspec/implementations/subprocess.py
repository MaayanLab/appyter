import os
import sys
import json
import asyncio
from appyter.execspec.spec import AbstractExecutor

class SubprocessExecutor(AbstractExecutor):
  ''' Run executions in a subprocess
  '''
  protocol = 'subprocess'

  async def _run(self, **job):
    yield dict(type='status', data=f"Launching job...")
    proc = await asyncio.create_subprocess_exec(
      sys.executable, '-u', '-m',
      'appyter', 'orchestration', 'job', json.dumps(job),
      stdout=sys.stdout,
      stderr=sys.stderr,
      env=dict(
        PYTHONPATH=':'.join(sys.path),
        PATH=os.environ['PATH'],
      ),
    )
    # TODO: capturing stdout here of nbexecute is probably better here
    #       than having the subprocess connect back over websocket
    await proc.wait()
    yield dict(type='status', data=f"Subprocess exited.")
