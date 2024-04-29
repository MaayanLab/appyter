import os
import traceback
import logging
from appyter.ext.json import try_json_loads
logger = logging.getLogger(__name__)

from appyter.execspec.spec import AbstractExecutor

class LocalExecutor(AbstractExecutor):
  ''' Run executions with the same process
  
  Not ideal in most circumstances:
  - it can leak errors to the notebook
  - internal state can get messed with
  '''
  protocol = 'local'

  def __init__(self, url=None, **kwargs) -> None:
    super().__init__(url=url, **kwargs)

  async def _submit(self, emit=None, **job):
    from appyter.render.nbexecute import nbexecute_async
    try:
      fuse = job.get('fuse')
      if fuse is None: fuse = try_json_loads(os.environ.get('APPYTER_FUSE'))
      if fuse is None: fuse = not job.get('debug', False)
      await nbexecute_async(
        cwd=f"storage://{job['cwd']}",
        ipynb=job['ipynb'],
        emit=emit,
        fuse=fuse,
      )
    except:
      logger.error(traceback.format_exc())
      await emit({ 'type': 'error', 'data': 'An error occurred while initializing the execution...' })
    finally:
      await emit(None)

  async def _run(self, **job):
    import asyncio
    from appyter.ext.fsspec.storage import ensure_storage
    async with ensure_storage(str(job.get('storage', 'file://'))):
      msg_queue = asyncio.Queue()
      task = asyncio.create_task(self._submit(emit=msg_queue.put, **job))
      while True:
        msg = await msg_queue.get()
        if msg: yield msg
        msg_queue.task_done()
        if not msg: break
      await task
