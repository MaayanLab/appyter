import os
import sys
import json
import traceback
import logging
logger = logging.getLogger()

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.subprocess import sh

class SubprocessExecutor(AbstractExecutor):
  ''' Run executions in a subprocess
  '''
  protocol = 'subprocess'

  async def _submit(self, **job):
    async for msg, done in sh(
      sys.executable, '-u', '-m',
      'appyter', 'nbexecute',
      '-w', f"storage://{job['cwd']}",
      '-s', 'file:///dev/stdout',
      '--data-dir', job['storage'],
      '--fuse=true',
      job['ipynb'],
      stderr=sys.stderr,
      env=dict(
        PYTHONPATH=':'.join(sys.path),
        PATH=os.environ['PATH'],
      ),
    ):
      yield msg, done

  async def _run(self, **job):
    yield dict(type='status', data=f"Launching subprocess...")
    async for msg, done in self._submit(**job):
      if not done:
        try: yield json.loads(msg)
        except: logger.warning(traceback.format_exc())
    if msg == 0:
      yield dict(type='status', data=f"Subprocess exited")
    else:
      yield dict(type='error', data=f"Subprocess exited with error code")
