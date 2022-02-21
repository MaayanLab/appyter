''' Async helpers to convert anything sync to and from anything async without deadlocks.
This requires that you initialize the event loop with the appyter.ext.asyncio.event_loop methods
 which will run the event loop in a dedicated thread and ensure all `sync` methods are executed
 on that dedicated event loop.
You only need to use `ensure_async` or `ensure_sync` these methods will deal with dispatching to
 the relevant handlers.
It works with already-sync/async, context managers, generators, & functions of these.
'''
import asyncio
import threading
import functools

from appyter.ext.asyncio.event_loop import get_event_loop

import logging
logger = logging.getLogger(__name__)

from inspect import (
  isasyncgen,
  isasyncgenfunction,
  isawaitable,
  iscoroutine,
  iscoroutinefunction,
  isfunction,
  isgenerator,
  isgeneratorfunction,
  ismethod,
)

def isasynccontextmanager(obj):
  return getattr(obj, '__aenter__', None) is not None

def iscontextmanager(obj):
  return getattr(obj, '__enter__', None) is not None

def _call(func, args, kwargs):
  return func(*args, **kwargs)

async def ensure_async_literal(obj):
  logger.debug(f"ensure_async_literal")
  return obj

async def awaitable_identity(obj):
  logger.debug(f"awaitable_identity")
  return await obj

def ensure_async_func(func):
  logger.debug(f"ensure_async_func")
  @functools.wraps(func)
  async def wrapper(*args, **kwargs):
    return await get_event_loop().run_in_executor(
      None,
      functools.partial(_call, func),
      args,
      kwargs,
    )
  return wrapper

@ensure_async_func
def anext(generator):
  logger.debug(f"anext")
  try:
    return next(generator)
  except StopIteration:
    raise StopAsyncIteration

async def ensure_async_generator(generator):
  logger.debug(f"ensure_async_generator")
  while True:
    try:
      await anext(generator)
    except StopAsyncIteration:
      break

def ensure_sync_coro(coro):
  logger.debug(f"ensure_sync_coro")
  loop = get_event_loop()
  done = threading.Event()
  future = asyncio.run_coroutine_threadsafe(coro, loop)
  future.add_done_callback(lambda *args, **kwargs: done.set())
  done.wait()
  return future.result()

def ensure_sync_generator(asyncgenerator):
  logger.debug(f"ensure_sync_generator")
  asyncgenerator_anext = functools.partial(ensure_sync_coro, asyncgenerator.__anext__)
  while True:
    try:
      yield asyncgenerator_anext()
    except StopAsyncIteration:
      break

class _AsyncSyncContextManager:
  def __init__(self, contextmanager):
    self._aenter = ensure_async(contextmanager.__enter__)
    self._aexit = ensure_async(contextmanager.__exit__)
  async def __aenter__(self):
    return await self._aenter()
  async def __aexit__(self, typ, value, traceback):
    return await self._aexit(typ, value, traceback)

def ensure_async_contextmanager(contextmanager):
  logger.debug(f"ensure_async_contextmanager")
  return _AsyncSyncContextManager(contextmanager)

class _SyncAsyncContextManager:
  def __init__(self, asynccontextmanager):
    self._enter = ensure_sync(asynccontextmanager.__aenter__)
    self._exit = ensure_sync(asynccontextmanager.__aexit__)
  def __enter__(self):
    return self._enter()
  def __exit__(self, typ, value, traceback):
    return self._exit(typ, value, traceback)

def ensure_sync_contextmanager(asynccontextmanager):
  logger.debug(f"ensure_sync_contextmanager")
  return _SyncAsyncContextManager(asynccontextmanager)

def ensure_async_wrapper(callable):
  logger.debug(f"ensure_async_wrapper")
  @functools.wraps(callable)
  def wrapper(*args, **kwargs):
    obj = callable(*args, **kwargs)
    return ensure_async(obj)
  return wrapper

def ensure_async(obj):
  if (
    iscoroutinefunction(obj)
    or isgeneratorfunction(obj)
  ):
    return ensure_async_wrapper(obj)
  elif (
    isasyncgen(obj)
    or isasyncgenfunction(obj)
    or iscoroutine(obj)
    or isawaitable(obj)
    or isasynccontextmanager(obj)
  ):
    return obj
  elif isgenerator(obj):
    return ensure_async_generator(obj)
  elif iscontextmanager(obj):
    return ensure_async_contextmanager(obj)
  elif ismethod(obj):
    return ensure_async_func(obj)
  elif isfunction(obj):
    return ensure_async_func(obj)
  else:
    return ensure_async_literal(obj)

def ensure_sync_wrapper(callable):
  logger.debug(f"ensure_sync_wrapper")
  @functools.wraps(callable)
  def wrapper(*args, **kwargs):
    obj = callable(*args, **kwargs)
    return ensure_sync(obj)
  return wrapper

def ensure_sync(obj):
  if (
    isasyncgenfunction(obj)
    or iscoroutinefunction(obj)
    or isgeneratorfunction(obj)
  ):
    return obj
  elif (
    ismethod(obj)
    or isfunction(obj)
  ):
    return ensure_sync_wrapper(obj)
  elif isasynccontextmanager(obj):
    return ensure_sync_contextmanager(obj)
  elif isasyncgen(obj):
    return ensure_sync_generator(obj)
  elif iscoroutine(obj):
    return ensure_sync_coro(obj)
  elif isawaitable(obj):
    return ensure_sync_coro(awaitable_identity(obj))
  else:
    return obj
