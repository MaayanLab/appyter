def run_in_executor(f):
  import asyncio
  import functools
  @functools.wraps(f)
  def inner(*args, **kwargs):
    loop = asyncio.get_running_loop()
    return loop.run_in_executor(None, lambda: f(*args, **kwargs))
  return inner
