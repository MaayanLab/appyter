import asyncio
import contextlib
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
  logger.getChild('sync_func').info(f"{a=} {b=} {c=}")
  return a

async def _async_func(a, b, c='d'):
  ''' An async function
  '''
  await asyncio.sleep(1)
  logger.getChild('async_func').info(f"{a=} {b=} {c=}")
  return b

def sync_async_func(a, b, c='d'):
  ''' A sync function that calls an async function
  '''
  ret = helpers.ensure_sync(_async_func)(a, b, c=c)
  logger.getChild('sync_async_func').info(f"sync_async {a=} {b=} {c=}")
  return ret

async def _test_call_sync_from_async():
  ''' Ensure these sync functions can be executed asynchronously
  '''
  assert 1 == await helpers.ensure_async(sync_func)(1, 2, c=3)
  assert 2 == await helpers.ensure_async(sync_async_func)(1, 2, c=3)

def test_call_sync_from_async():
  ''' Test calling the asynchronous test suite
  '''
  helpers.ensure_sync(_test_call_sync_from_async)()


@contextlib.contextmanager
def _sync_context_manager():
  yield 1

@contextlib.asynccontextmanager
async def _async_context_manager():
  asyncio.sleep(1)
  async with helpers.ensure_async(_sync_context_manager)() as v:
    yield v

def test_syned_ctxmanager():
  with helpers.ensure_sync(_async_context_manager)() as v:
    assert v == 1
