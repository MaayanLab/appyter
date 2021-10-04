from appyter.ext.fs import Filesystem

async def storage_ctx(app):
  data_dir = app['config']['DATA_DIR']
  storage = Filesystem(data_dir)
  Filesystem.protocols['storage'] = lambda url, **kwargs: storage.chroot(url.path, **kwargs)
  yield
