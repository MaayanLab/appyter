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

  async def __aenter__(self):
    proc = await asyncio.create_subprocess_exec(*[
      'docker', 'inspect', os.environ['HOSTNAME'],
    ], stdout=asyncio.subprocess.PIPE)
    proc_stdout, _ = await proc.communicate()
    conf = json.loads(proc_stdout.decode())
    self._args = [
      'docker', 'run',
      '--device', '/dev/fuse',
      '--cap-add', 'SYS_ADMIN',
      '--security-opt', 'apparmor:unconfined',
      '--network', conf[0]['HostConfig']['NetworkMode']
    ]
    return await super().__aenter__()

  async def _run(self, **job):
    yield dict(type='status', data=f"Launching container...")
    proc = await asyncio.create_subprocess_exec(
      *self._args, job['image'],
      'appyter', 'orchestration', 'job', json.dumps(job),
      stdout=sys.stdout,
      stderr=sys.stderr,
    )
    # TODO: capturing stdout here of nbexecute is probably better here
    #       than having the subprocess connect back over websocket
    await proc.wait()
    yield dict(type='status', data=f"Container exited.")
