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
    await nbexecute_async(
      cwd=job['cwd'],
      ipynb=job['ipynb'],
      emit=emit,
      fuse=not job.get('debug', False),
    )
    await emit(None)

  async def _run(self, **job):
    import asyncio
    msg_queue = asyncio.Queue()
    task = asyncio.create_task(self._submit(emit=msg_queue.put, **job))
    while True:
      msg = await msg_queue.get()
      if msg: yield msg
      msg_queue.task_done()
      if not msg: break
    await task
