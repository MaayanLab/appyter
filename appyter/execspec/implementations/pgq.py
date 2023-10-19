import asyncio
from appyter.execspec.spec import AbstractExecutor
from appyter.orchestration.pg.schema import schema

class PGQExecutor(AbstractExecutor):
  ''' Submit executions to a postgres database

  This executor submits jobs to a queue which manages the execution.
  
  usage:
  pgq::psql://user:pass@pghost/db?params.executor=docker::maayanlab/appyter-example:latest
  '''
  protocol = 'pgq'

  async def __aenter__(self):
    import aiopg
    self.pool_ctx = aiopg.create_pool(self.url)
    self.pool = await self.pool_ctx.__aenter__()
    async with self.pool.acquire() as conn:
      try:
        async with conn.cursor() as cur:
          await cur.execute(schema)
      except KeyboardInterrupt: raise
      except asyncio.CancelledError: raise
      except: pass # creating this schema/table will fail if it already exists
    return await super().__aenter__()
  
  async def __aexit__(self, type, value, traceback):
    await self.pool_ctx.__aexit__(type, value, traceback)
    await super().__aexit__(type, value, traceback)

  async def _submit(self, job):
    async with self.pool.acquire() as conn:
      async with conn.cursor() as cur:
        cur = await cur.execute('''
          select pgq.put($1);
        ''', (job,))
        async for id, pos in cur:
          return id, pos

  async def _task_position(self, id):
    async with self.pool.acquire() as conn:
      async with conn.cursor() as cur:
        cur = await cur.execute('''
          select pgq.task_position($1);
        ''', (id,))
        async for pos, in cur:
          return pos

  async def _run(self, **job):
    yield dict(type='status', data=f"Submitting appyter for execution..")
    id, pos = await self._submit(job)
    yield dict(type='status', data=f"Queued successfully, you are at position {pos}, your execution will begin when resources are available..")
    async with self.pool.acquire() as conn:
      async with conn.cursor() as cur:
        await cur.execute("listen pgq")
        while True:
          msg = await conn.notifies.get()
          _channel, msg_id, msg_kind = msg.payload.split(' ')
          if msg_kind == 'pop':
            if msg != id:
              new_pos = await self._task_position(id)
              if new_pos != pos:
                pos = new_pos
                yield dict(type='status', data=f"Queued successfully, you are at position {pos}, your execution will begin when resources are available..")
              else:
                yield dict(type='status', data=f"Your execution is starting...")
          elif msg_id == id and msg_kind == 'task_done':
            break
    yield dict(type='status', data=f"Job completed.")
