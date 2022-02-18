import asyncio
from appyter.ext.asyncio import helpers

import logging

logger = logging.getLogger(__name__)

import pytest
@pytest.fixture(scope="session", autouse=True)
def setup():
  from appyter.ext.asyncio.event_loop import new_event_loop
  loop = new_event_loop()
  yield
  loop.close()

def sync_func(a, b, c='d'):
  ''' Your standard synchronous python function
  '''
  logger.getChild('ync_func').info(f"{a=} {b=} {c=}")

async def _async_func(a, b, c='d'):
  ''' An async function
  '''
  await asyncio.sleep(1)
  logger.getChild('async_func').info(f"{a=} {b=} {c=}")

def sync_async_func(a, b, c='d'):
  ''' A sync function that calls an async function
  '''
  helpers.ensure_sync(_async_func)(a, b, c=c)
  logger.getChild('sync_async_func').info(f"sync_async {a=} {b=} {c=}")

async def _test_call_sync_from_async():
  ''' Ensure these sync functions can be executed asynchronously
  '''
  await helpers.ensure_async(sync_func)(1, 2, c=3)
  await helpers.ensure_async(sync_async_func)(1, 2, c=3)

def test_call_sync_from_async():
  ''' Test calling the asynchronous test suite
  '''
  helpers.ensure_sync(_test_call_sync_from_async)()
