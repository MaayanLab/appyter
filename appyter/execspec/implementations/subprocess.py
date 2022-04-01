import os
import sys
import json
import asyncio
from appyter.execspec.spec import AbstractExecutor

class SubprocessExecutor(AbstractExecutor):
  ''' Run executions in a subprocess
  '''
  protocol = 'subprocess'

  async def _submit(self, **job):
    proc = await asyncio.create_subprocess_exec(
      sys.executable, '-u', '-m',
      'appyter', 'nbexecute',
      '--cwd', job['cwd'],
      '--data-dir', str(job['storage']),
      job['ipynb'],
      stdout=asyncio.subprocess.PIPE,
      stderr=sys.stderr,
      env=dict(
        PYTHONPATH=':'.join(sys.path),
        PATH=os.environ['PATH'],
      ),
    )
    while True:
      line = await proc.stdout.readline()
      if not line: break
      yield json.loads(line), False
    yield await proc.wait(), True

  async def _run(self, **job):
    yield dict(type='status', data=f"Launching subprocess...")
    async for msg, done in self._submit(**job):
      if not done: yield msg
    if msg == 0:
      yield dict(type='status', data=f"Subprocess exited")
    else:
      yield dict(type='error', data=f"Subprocess exited with error code")
