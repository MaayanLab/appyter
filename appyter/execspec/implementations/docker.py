import os
import sys
import json
import logging
import asyncio

logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.dict import dict_merge

class DockerExecutor(AbstractExecutor):
  ''' Run executions in a docker job
  Example uri:
  docker::maayanlab/myimage:latest?flags.v=/mydatadir:/data&args.data-dir=/data
  '''
  protocol = 'docker'

  async def __aenter__(self):
    self._args = [
      'docker', 'run',
      *(
        f"--{k}={v}" if len(k) > 1 else f"-{k}{v}"
        for k, v in self.executor_options.get('flags', {}).items()
      ),
      self.url,
    ]
    try:
      proc = await asyncio.create_subprocess_exec(*[
        'docker', 'inspect', os.environ['HOSTNAME'],
      ], stdout=asyncio.subprocess.PIPE)
      proc_stdout, _ = await proc.communicate()
      conf = json.loads(proc_stdout.decode())
      self._args += [
        '--network', conf[0]['HostConfig']['NetworkMode']
      ]
    except:
      logger.warn('Not a docker container')
    return await super().__aenter__()

  async def _submit(self, **job):
    full_args = [
      *self._args,
      'appyter', 'nbexecute',
      *(
        f"--{k}={v}" if len(k) > 1 else f"-{k}{v}"
        for k, v in dict_merge(
          {
            'cwd': job['cwd'],
            'data-dir': str(job['storage']),
          },
          **self.executor_options.get('args', {})
        ).items()
      ),
      job['ipynb'],
    ]
    logger.debug(' '.join(map(repr, full_args)))
    proc = await asyncio.create_subprocess_exec(
      *full_args,
      stdout=asyncio.subprocess.PIPE,
      stderr=sys.stderr,
    )
    while True:
      line = await proc.stdout.readline()
      if not line: break
      yield json.loads(line), False
    yield await proc.wait(), True

  async def _run(self, **job):
    yield dict(type='status', data=f"Launching container...")
    async for msg, done in self._submit(**job):
      if not done: yield msg
    if msg == 0:
      yield dict(type='status', data=f"Container exited")
    else:
      yield dict(type='error', data=f"Container exited with error code")
