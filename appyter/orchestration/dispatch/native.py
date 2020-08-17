''' Launch job natively using python
'''

import sys
import json

def dispatch(job=None, Popen=None, **kwargs):
  with Popen([
    sys.executable, '-u',
    '-m', 'appyter', 'orchestration', 'job', json.dumps(job)
  ]) as proc:
    return proc.wait()
