''' Launch job using docker directly
'''

import json

def dispatch(job=None, Popen=None, **kwargs):
  with Popen([
    'docker', 'run',
    '-it', job['image'],
    'appyter', 'orchestration', 'job', json.dumps(job)
  ]) as proc:
    proc.wait()
