import inspect
import functools
import logging
import asyncio
import threading

from appyter.ext.asyncio.event_loop import get_event_loop

logger = logging.getLogger(__name__)

def arg_compressor(func):
  @functools.wraps(func)
  def wrapper(args, kwargs):
    return func(*args, **kwargs)
  return wrapper

def isasynccontextmanager(obj):
  return getattr(obj, '__aenter__', None) is not None

def iscontextmanager(obj):
  return getattr(obj, '__enter__', None) is not None

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
    return await get_event_loop().run_in_executor(None, arg_compressor(func), args, kwargs)
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
    return self._aenter()
  async def __aexit__(self, *args):
    return self._aexit(*args)

def ensure_async_contextmanager(contextmanager):
  logger.debug(f"ensure_async_contextmanager")
  return _AsyncSyncContextManager(contextmanager)

class _SyncAsyncContextManager:
  def __init__(self, asynccontextmanager):
    self._enter = ensure_sync(asynccontextmanager.__aenter__)
    self._exit = ensure_sync(asynccontextmanager.__aexit__)
  def __enter__(self):
    return self._enter()
  def __exit__(self, *args):
    return self._exit(*args)

def ensure_sync_contextmanager(asynccontextmanager):
  logger.debug(f"ensure_sync_contextmanager")
  return _SyncAsyncContextManager(asynccontextmanager)

def _ensure_async_helper(callable):
  logger.debug(f"_ensure_async_helper")
  @functools.wraps(callable)
  def wrapper(*args, **kwargs):
    obj = callable(*args, **kwargs)
    return ensure_async(obj)
  return wrapper

def ensure_async(obj):
  if (
    inspect.isasyncgenfunction(obj)
    or inspect.iscoroutinefunction(obj)
    or inspect.isgeneratorfunction(obj)
  ):
    return _ensure_async_helper(obj)
  elif (
    inspect.isasyncgen(obj)
    or inspect.iscoroutine(obj)
    or inspect.isawaitable(obj)
    or isasynccontextmanager(obj)
  ):
    return obj
  elif inspect.isgenerator(obj):
    return ensure_async_generator(obj)
  elif iscontextmanager(obj):
    return ensure_async_contextmanager(obj)
  elif inspect.isfunction(obj) or inspect.ismethod(obj):
    return ensure_async_func(obj)
  else:
    logger.warn(f"fallthrough: {obj}")
    return ensure_async_literal(obj)

def _ensure_sync_helper(callable):
  logger.debug(f"_ensure_sync_helper")
  @functools.wraps(callable)
  def wrapper(*args, **kwargs):
    obj = callable(*args, **kwargs)
    return ensure_sync(obj)
  return wrapper

def ensure_sync(obj):
  if (
    inspect.isasyncgenfunction(obj)
    or inspect.iscoroutinefunction(obj)
    or inspect.isgeneratorfunction(obj)
    or inspect.isfunction(obj)
    or inspect.ismethod(obj)
  ):
    return _ensure_sync_helper(obj)
  elif isasynccontextmanager(obj):
    return ensure_sync_contextmanager(obj)
  elif inspect.isasyncgen(obj):
    return ensure_sync_generator(obj)
  elif inspect.iscoroutine(obj):
    return ensure_sync_coro(obj)
  elif inspect.isawaitable(obj):
    return ensure_sync_coro(awaitable_identity(obj))
  else:
    return obj
