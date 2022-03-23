import time
import asyncio
import contextlib
from appyter.ext.asyncio import helpers
from appyter.ext.itertools import alist

import logging

logger = logging.getLogger(__name__)

import pytest
from appyter.ext.pytest import assert_eq, assert_exc
from appyter.ext.asyncio.event_loop import with_event_loop
@pytest.fixture(scope="session", autouse=True)
def event_loop_fixture():
  with with_event_loop():
    yield

@contextlib.asynccontextmanager
async def asyncctx(a, *, b=1):
  await asyncio.sleep(0.1)
  yield a+b

async def asyncgenfun(a, *, b=1):
  yield a
  await asyncio.sleep(0.1)
  yield a+b

async def asyncfun(a, *, b=1):
  await asyncio.sleep(0.1)
  return a+b

@contextlib.contextmanager
def syncctx(a, *, b=1):
  time.sleep(0.1)
  yield a+b

def syncgenfun(a, *, b=1):
  yield a
  time.sleep(0.1)
  yield a+b

def syncfun(a, *, b=1):
  time.sleep(0.1)
  return a+b

async def async_mixedfun(a, *, b=1):
  return await helpers.ensure_async(syncfun(a, b=b))

def sync_exc():
  logger.info("Sync: Raising Runtime Error")
  raise RuntimeError()

async def async_exc():
  logger.info("Async: Raising Runtime Error")
  raise RuntimeError()

def test_ensure_sync_async_ctx():
  with helpers.ensure_sync(asyncctx(1)) as ctx: assert_eq(ctx, 2)
  with helpers.ensure_sync(asyncctx)(0,b=2) as ctx: assert_eq(ctx, 2)

def test_ensure_sync_async_gen():
  assert_eq(list(helpers.ensure_sync(asyncgenfun)(1)), [1,2])
  assert_eq(list(helpers.ensure_sync(asyncgenfun(0,b=2))), [0,2])

def test_ensure_sync_async_fun():
  assert_eq(helpers.ensure_sync(asyncfun)(1), 2)
  assert_eq(helpers.ensure_sync(asyncfun(0,b=2)), 2)

def test_ensure_sync_async_exc():
  with assert_exc(RuntimeError):
    helpers.ensure_sync(async_exc)()

def test_ensure_sync_sync_ctx():
  i = 0
  with helpers.ensure_sync(syncctx(1)) as ctx:
    assert_eq(ctx, 2)
    i += 1
  with helpers.ensure_sync(syncctx)(0,b=2) as ctx:
    assert_eq(ctx, 2)
    i += 1
  assert_eq(i, 2)

def test_ensure_sync_sync_gen():
  assert_eq(list(helpers.ensure_sync(syncgenfun)(1)), [1,2])
  assert_eq(list(helpers.ensure_sync(syncgenfun(0,b=2))), [0,2])

def test_ensure_sync_sync_fun():
  assert_eq(helpers.ensure_sync(syncfun)(1), 2)
  assert_eq(helpers.ensure_sync(syncfun(0,b=2)), 2)

def test_ensure_sync_sync_exc():
  with assert_exc(RuntimeError):
    helpers.ensure_sync(sync_exc)()

def test_ensure_sync_mixed_fun():
  assert_eq(helpers.ensure_sync(async_mixedfun(0,b=2)), 2)

async def _test_ensure_async_async_ctx():
  i = 0
  async with helpers.ensure_async(asyncctx(1)) as ctx:
    i += 1
    assert_eq(ctx, 2)
  # Not supported
  # async with helpers.ensure_async(asyncctx)(0,b=2) as ctx: assert_eq(ctx, 2)
  assert_eq(i, 1)
def test_ensure_async_async_ctx():
  helpers.ensure_sync(_test_ensure_async_async_ctx)()

async def _test_ensure_async_async_gen():
  assert_eq(await alist(helpers.ensure_async(asyncgenfun)(1)), [1,2])
  assert_eq(await alist(helpers.ensure_async(asyncgenfun(0,b=2))), [0,2])
def test_ensure_async_async_gen():
  helpers.ensure_sync(_test_ensure_async_async_gen)()

async def _test_ensure_async_async_fun():
  assert_eq(await helpers.ensure_async(asyncfun)(1), 2)
  assert_eq(await helpers.ensure_async(asyncfun(0,b=2)), 2)
def test_ensure_async_async_fun():
  helpers.ensure_sync(_test_ensure_async_async_fun)()

async def _test_ensure_async_async_exc():
  with assert_exc(RuntimeError):
    await helpers.ensure_async(async_exc)()
def test_ensure_async_async_exc():
  helpers.ensure_sync(_test_ensure_async_async_exc)()

async def _test_ensure_async_sync_ctx():
  i = 0
  async with helpers.ensure_async(syncctx(1)) as ctx:
    i += 1
    assert_eq(ctx, 2)
  # Not supported
  # async with helpers.ensure_async(syncctx)(0,b=2) as ctx: assert_eq(ctx, 2)
  assert_eq(i, 1)

def test_ensure_async_sync_ctx():
  helpers.ensure_sync(_test_ensure_async_sync_ctx)()

async def _test_ensure_async_sync_gen():
  assert_eq(await alist(helpers.ensure_async(syncgenfun)(1)), [1,2])
  assert_eq(await alist(helpers.ensure_async(syncgenfun(0,b=2))), [0,2])
def test_ensure_async_sync_gen():
  helpers.ensure_sync(_test_ensure_async_sync_gen)()

async def _test_ensure_async_sync_fun():
  assert_eq(await helpers.ensure_async(syncfun)(1), 2)
  assert_eq(await helpers.ensure_async(syncfun(0,b=2)), 2)
def test_ensure_async_sync_fun():
  helpers.ensure_sync(_test_ensure_async_sync_fun)()

async def _test_ensure_async_sync_exc():
  with assert_exc(RuntimeError):
    await helpers.ensure_async(sync_exc)()
def test_ensure_async_sync_exc():
  helpers.ensure_sync(_test_ensure_async_sync_exc)()

async def _test_ensure_async_mixed_fun():
  assert_eq(await helpers.ensure_async(async_mixedfun(0,b=2)), 2)
def test_ensure_async_mixed_fun():
  helpers.ensure_sync(_test_ensure_async_mixed_fun)()

async def _test_async_sync_bottom_up_exc():
  try:
    await helpers.ensure_async(sync_exc)()
  except RuntimeError as e:
    assert isinstance(e, RuntimeError)
    logger.info(f"Async: Received {repr(e)}, Re-raising")
    raise

def test_async_sync_bottom_up_exc():
  with assert_exc(RuntimeError):
    logger.info("Starting async_sync_exc")
    helpers.ensure_sync(_test_async_sync_bottom_up_exc)()
    logger.info("Done.")


@contextlib.asynccontextmanager
async def _test_async_sync_top_down_exc():
  try:
    yield
  except KeyboardInterrupt as e:
    assert isinstance(e, KeyboardInterrupt)
    logger.info(f"Async: Received {repr(e)}, Re-raising")
    raise

def test_async_sync_top_down_exc():
  with assert_exc(KeyboardInterrupt):
    with helpers.ensure_sync(_test_async_sync_top_down_exc()):
      time.sleep(0.5)
      raise KeyboardInterrupt


def test_async_sync_async_ctx():
  class MyAsynCls:
    def __init__(self):
      logger.debug("MyAsynCls()")

    async def __aenter__(self):
      logger.debug("MyAsynCls.__aenter__")
      await asyncio.sleep(0.1)
      return self
    async def __aexit__(self, *args):
      logger.debug("MyAsynCls.__aexit__")
      await asyncio.sleep(0.1)
  class MySynCls:
    def __init__(self):
      logger.debug("MySynCls()")
      self.asyn = MyAsynCls()

    def __enter__(self):
      logger.debug("MySynCls.__enter__")
      helpers.ensure_sync(self.asyn.__aenter__())
      time.sleep(0.1)

    def __exit__(self, *args):
      helpers.ensure_sync(self.asyn.__aexit__(*args))
      time.sleep(0.1)
      logger.debug("MySynCls.__exit__")

  async def _test():
    syn = MySynCls()
    logger.debug("with MySynCls")
    # with syn: # NOTE: this would cause a hang
    async with helpers.ensure_async(syn):
      logger.debug("entered")
      await asyncio.sleep(0.1)
      logger.debug("exited")
  helpers.ensure_sync(_test())
