from appyter.ext.fs import Filesystem

async def storage_ctx(app):
  data_dir = app['config']['DATA_DIR']
  storage = Filesystem(data_dir)
  Filesystem.protocols['storage'] = lambda uri, **kwargs: Filesystem.chroot(storage, uri.path, **kwargs)
  yield
