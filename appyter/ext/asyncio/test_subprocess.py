import asyncio
import itertools
from appyter.ext.pytest import assert_eq
from appyter.ext.asyncio.subprocess import sh

async def _test_subprocess(expectation, chunk_size=None):
  i = iter(itertools.count())
  async for msg, done in sh('cat', __file__, chunk_size=chunk_size):
    assert_eq(msg, expectation[next(i)])

def test_subprocess():
  with open(__file__, 'rb') as fr:
    expectation = fr.readlines()
  expectation.append(0)
  # ensure it works with lines bigger than chunk_size
  asyncio.new_event_loop().run_until_complete(_test_subprocess(expectation, chunk_size=5))
  # ensure it works with chunks bigger than the lines
  asyncio.new_event_loop().run_until_complete(_test_subprocess(expectation, chunk_size=len(expectation)*2))
