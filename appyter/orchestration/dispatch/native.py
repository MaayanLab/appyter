''' Launch job natively using python
'''

import os
import sys
import json

def dispatch(job=None, Popen=None, **kwargs):
  with Popen([
    sys.executable, '-u',
    '-m', 'appyter', 'orchestration', 'job', json.dumps(job)
  ], env=dict(
    PYTHONPATH=':'.join(sys.path),
    PATH=os.environ['PATH'],
  )) as proc:
    return proc.wait()
