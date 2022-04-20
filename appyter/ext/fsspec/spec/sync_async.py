from appyter.ext.asyncio.helpers import ensure_sync

class SyncAsyncFileSystem:
  ''' A helper for fsspec AsyncFileSystems to use our own
  `ensure_sync` for all sync methods.
  '''
  def __enter__(self):
    if getattr(self, '__aenter__', None) is not None:
      return ensure_sync(self.__aenter__())
    elif getattr(super(), '__enter__', None) is not None:
      return super().__enter__()
    else:
      raise NotImplementedError

  def __exit__(self, *args):
    if getattr(self, '__aexit__', None) is not None:
      return ensure_sync(self.__aexit__(*args))
    elif getattr(super(), '__exit__', None) is not None:
      return super().__exit__(*args)
    else:
      raise NotImplementedError

  def mkdir(self, *args, **kwargs):
    if getattr(self, '_mkdir', None) is not None:
      return ensure_sync(self._mkdir(*args, **kwargs))
    elif getattr(super(), 'mkdir', None) is not None:
      return super().mkdir(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def makedirs(self, *args, **kwargs):
    if getattr(self, '_makedirs', None) is not None:
      return ensure_sync(self._makedirs(*args, **kwargs))
    elif getattr(super(), 'makedirs', None) is not None:
      return super().makedirs(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def rmdir(self, *args, **kwargs):
    if getattr(self, '_rmdir', None) is not None:
      return ensure_sync(self._rmdir(*args, **kwargs))
    elif getattr(super(), 'rmdir', None) is not None:
      return super().rmdir(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def rm_file(self, *args, **kwargs):
    if getattr(self, '_rm_file', None) is not None:
      return ensure_sync(self._rm_file(*args, **kwargs))
    elif getattr(super(), 'rm_file', None) is not None:
      return super().rm_file(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def rm(self, *args, **kwargs):
    if getattr(self, '_rm', None) is not None:
      return ensure_sync(self._rm(*args, **kwargs))
    elif getattr(super(), 'rm', None) is not None:
      return super().rm(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def mv(self, *args, **kwargs):
    if getattr(self, '_mv', None) is not None:
      return ensure_sync(self._mv(*args, **kwargs))
    elif getattr(super(), 'mv', None) is not None:
      return super().mv(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def cp_file(self, *args, **kwargs):
    if getattr(self, '_cp_file', None) is not None:
      return ensure_sync(self._cp_file(*args, **kwargs))
    elif getattr(super(), 'cp_file', None) is not None:
      return super().cp_file(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def cat_file(self, *args, **kwargs):
    if getattr(self, '_cat_file', None) is not None:
      return ensure_sync(self._cat_file(*args, **kwargs))
    elif getattr(super(), 'cat_file', None) is not None:
      return super().cat_file(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def put_file(self, *args, **kwargs):
    if getattr(self, '_put_file', None) is not None:
      return ensure_sync(self._put_file(*args, **kwargs))
    elif getattr(super(), 'put_file', None) is not None:
      return super().put_file(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def get_file(self, *args, **kwargs):
    if getattr(self, '_get_file', None) is not None:
      return ensure_sync(self._get_file(*args, **kwargs))
    elif getattr(super(), 'get_file', None) is not None:
      return super().get_file(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def exists(self, *args, **kwargs):
    if getattr(self, '_exists', None) is not None:
      return ensure_sync(self._exists(*args, **kwargs))
    elif getattr(super(), 'exists', None) is not None:
      return super().exists(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def info(self, *args, **kwargs):
    if getattr(self, '_info', None) is not None:
      return ensure_sync(self._info(*args, **kwargs))
    elif getattr(super(), 'info', None) is not None:
      return super().info(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def ls(self, *args, **kwargs):
    if getattr(self, '_ls', None) is not None:
      return ensure_sync(self._ls(*args, **kwargs))
    elif getattr(super(), 'ls', None) is not None:
      return super().ls(*args, **kwargs)
    else:
      raise NotImplementedError
  
  def glob(self, *args, **kwargs):
    if getattr(self, '_glob', None) is not None:
      return ensure_sync(self._glob(*args, **kwargs))
    elif getattr(super(), 'glob', None) is not None:
      return super().glob(*args, **kwargs)
    else:
      raise NotImplementedError
