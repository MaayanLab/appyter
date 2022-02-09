from pathlib import Path

from appyter.ext.asyncio.run_in_executor import run_in_executor

def assert_mounted(path: Path):
  assert path.is_mount()
async_assert_mounted = run_in_executor(assert_mounted)

def assert_unmounted(path: Path):
  assert not path.is_mount()
async_assert_unmounted = run_in_executor(assert_unmounted)

def assert_exists(path: Path):
  assert path.exists()
async_assert_exists = run_in_executor(assert_exists)
