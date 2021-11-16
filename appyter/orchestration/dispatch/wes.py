''' Launch job via WES
'''

import json
import random
import asyncio
import aiohttp
import logging
logger = logging.getLogger(__name__)
from appyter.ext.dict import dict_merge
from appyter.ext.urllib import join_slash

async def dispatch(job=None,
  api_endpoint='https://cavatica-ga4gh-api.sbgenomics.com/ga4gh/wes/v1',
  params=dict(
    workflow_params=dict(
      project=''
    ),
    workflow_type='CWL',
    workflow_type_version='v1.2',
    tags='appyter',
  ),
  headers={},
  **kwargs,
):
  ''' WES dispatcher -- submit job via CWL to WES endpoint
  '''
  async with aiohttp.ClientSession() as session:
    logger.info(f"Submitting {job} to {api_endpoint}")
    async with session.post(
      join_slash(api_endpoint, '/runs'),
      data=json.dumps(dict_merge(
        params,
        workflow_params=dict(
          inputs=job,
        ),
        workflow_url='#/workflow_attachment/0', #TODO: possibly store this ahead of time via sbfs
        workflow_attachment=[
          # TODO: create CWL & insert here
        ],
      )),
      headers=headers,
    ) as req:
      res = await req.json()
      run_id = res['run_id']
    #
    while True:
      await asyncio.sleep(30 * (0.5 + random.random()))
      logger.debug(f"Checking status of job {run_id=}")
      async with session.get(join_slash(api_endpoint, run_id, 'status'), headers=headers) as req:
        res = await req.json()
        state = res['state']
      logger.debug(f"{state=}")
      #
      if state == 'COMPLETE':
        return 0
      elif state == 'CANCELED':
        return 1
      elif state == 'EXECUTOR_ERROR':
        return -1
