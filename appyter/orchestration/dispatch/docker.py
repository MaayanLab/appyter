''' Launch job using docker directly
'''

import os
import json
from subprocess import PIPE

def dispatch(job=None, Popen=None, **kwargs):
  args = ['docker', 'run']
  args += ['--device', '/dev/fuse']
  args += ['--cap-add', 'SYS_ADMIN']
  args += ['--security-opt', 'seccomp=unconfined']
  try:
    with Popen([
      'docker', 'inspect', os.environ['HOSTNAME'],
    ], stdout=PIPE) as proc:
      conf = json.load(proc.stdout)
    args += ['--network', conf[0]['HostConfig']['NetworkMode']]
  except:
    args += []
  #
  args += [
    job['image'],
    'appyter', 'orchestration', 'job', json.dumps(job),
  ]
  with Popen(args) as proc:
    proc.wait()
