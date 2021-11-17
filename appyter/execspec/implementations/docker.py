import os
import sys
import json
import logging
import asyncio
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor

class DockerExecutor(AbstractExecutor):
  ''' Run executions in a docker job
  '''
  protocol = 'docker'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)
    self._procs = {}
    self._args = [
      'docker', 'run',
      '--device', '/dev/fuse',
      '--cap-add', 'SYS_ADMIN',
    ]

  async def __aenter__(self):
    try:
      proc = await asyncio.create_subprocess_exec(*[
        'docker', 'inspect', os.environ['HOSTNAME'],
      ], stdout=asyncio.subprocess.PIPE)
      proc_stdout, _ = await proc.communicate()
      conf = json.loads(proc_stdout.decode())
      self._args += ['--network', conf[0]['HostConfig']['NetworkMode']]
    except:
      import traceback
      logger.warn(traceback.format_exc())
    return self

  async def __aexit__(self, type, value, traceback):
    pass

  async def submit(self, job):
    self._procs[job['id']] = await asyncio.create_subprocess_exec(
      *self._args, job['image'],
      'appyter', 'orchestration', 'job', json.dumps(job),
      stdout=sys.stdout,
      stderr=sys.stderr,
    )
    return job['id']

  async def wait_for(self, run_id):
    return await (self._procs.pop(run_id)).wait()
