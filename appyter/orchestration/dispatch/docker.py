''' Launch job using docker directly
'''

import os
import sys
import json
import asyncio
from subprocess import PIPE

async def dispatch(job=None, **kwargs):
  args = ['docker', 'run']
  args += ['--device', '/dev/fuse']
  args += ['--privileged']
  try:
    proc = await asyncio.create_subprocess_exec(*[
      'docker', 'inspect', os.environ['HOSTNAME'],
    ], stdout=asyncio.subprocess.PIPE)
    proc_stdout, _ = await proc.communicate()
    conf = json.load(proc_stdout)
    args += ['--network', conf[0]['HostConfig']['NetworkMode']]
  except:
    args += []
  #
  args += [
    job['image'],
    'appyter', 'orchestration', 'job', json.dumps(job),
  ]
  proc = await asyncio.create_subprocess_exec(*args, stdout=sys.stdout, stderr=sys.stderr)
  return await proc.wait()
