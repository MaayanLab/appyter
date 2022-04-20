import os
import sys
import json
import logging
import asyncio
import traceback

logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor
from appyter.ext.asyncio.subprocess import sh
from appyter.ext.dict import dict_merge
from appyter.ext.json import async_json_loads

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
        for k, v in dict_merge({
          'device': '/dev/fuse',
          'cap-add': 'SYS_ADMIN',
          'security-opt': 'apparmor:unconfined',
        }, **self.executor_options.get('flags', {})).items()
      ),
    ]
    try:
      proc = await asyncio.create_subprocess_exec(*[
        'docker', 'inspect', os.environ['HOSTNAME'],
      ], stdout=asyncio.subprocess.PIPE)
      proc_stdout, _ = await proc.communicate()
      conf = await async_json_loads(proc_stdout.decode())
      self._args += [
        f"--network={conf[0]['HostConfig']['NetworkMode']}"
      ]
    except:
      logger.warn('Not a docker container')
    self._args.append(self.url)
    return await super().__aenter__()

  async def _submit(self, **job):
    full_args = [
      *self._args,
      'appyter', 'nbexecute',
      *(
        f"--{k}={v}" if len(k) > 1 else f"-{k}{v}"
        for k, v in dict_merge(
          {
            'w': f"storage://{job['cwd']}",
            's': 'file:///dev/stdout',
            'fuse': 'true',
            'data-dir': job['storage'],
          },
          **self.executor_options.get('args', {})
        ).items()
      ),
      job['ipynb'],
    ]
    async for msg, done in sh(*full_args, stderr=sys.stderr):
      yield msg, done

  async def _run(self, **job):
    yield dict(type='status', data=f"Launching container...")
    async for msg, done in self._submit(**job):
      if not done:
        try: yield await async_json_loads(msg)
        except: logger.warning(traceback.format_exc())
    if msg != 0:
      yield dict(type='error', data=f"Container exited with error code")
