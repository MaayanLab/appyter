import asyncio
import aiohttp, aiohttp.web
import contextlib
import logging
from appyter.ext.asyncio.helpers import ensure_sync

logger = logging.getLogger(__name__)

@contextlib.asynccontextmanager
async def with_app_running(app, host='127.0.0.1', port=5000, path=None, ssl_context=None):
  runner = aiohttp.web.AppRunner(app)
  await runner.setup()
  if path:
    site = aiohttp.web.UnixSite(runner, path, ssl_context=ssl_context)
    logger.info(f"Starting server at unix://{path}")
  elif port is not None:
    site = aiohttp.web.TCPSite(runner, host, port, ssl_context=ssl_context)
    logger.info(f"Starting server on http://{host}:{port}")
  else:
    raise NotImplementedError
  await site.start()
  try:
    yield
  finally:
    logger.info(f"Cleaning up server...")
    await runner.cleanup()

@ensure_sync
async def run_app(app, host='127.0.0.1', port=5000, path=None):
  async with with_app_running(app, host=host, port=port, path=path):
    try:
      await asyncio.Event().wait()
    except asyncio.CancelledError:
      pass
