async def storage_ctx(app):
  data_dir = app['config']['DATA_DIR']
  import fsspec
  from appyter.ext.fsspec.alias import AliasFileSystemFactory
  fsspec.register_implementation('storage', AliasFileSystemFactory('storage', data_dir))
  yield
