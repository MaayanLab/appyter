''' Launch job natively using python
'''

import os
import sys
import json
import asyncio

async def dispatch(job=None, **kwargs):
  proc = await asyncio.create_subprocess_exec(*[
    sys.executable, '-u',
    '-m', 'appyter', 'orchestration', 'job', json.dumps(job)
  ], env=dict(
    PYTHONPATH=':'.join(sys.path),
    PATH=os.environ['PATH'],
  ), stdout=sys.stdout, stderr=sys.stderr)
  return await proc.wait()
