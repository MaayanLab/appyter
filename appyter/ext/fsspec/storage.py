import contextlib

@contextlib.asynccontextmanager
async def ensure_storage(storage_uri):
  import fsspec
  from appyter.ext.fsspec.core import url_to_fs_ex
  if 'storage' not in fsspec.registry.target:
    from appyter.ext.fsspec.singleton import SingletonFileSystem
    from appyter.ext.asyncio.helpers import ensure_async_contextmanager
    fs, fo = url_to_fs_ex(storage_uri)
    async with ensure_async_contextmanager(SingletonFileSystem(proto='storage', fs=fs, fo=fo)) as fs:
      yield fs
  else:
    fs, _ = url_to_fs_ex('storage://')
    yield fs
