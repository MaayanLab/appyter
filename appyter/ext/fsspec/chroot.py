from pathlib import PurePosixPath
from fsspec import filesystem, AbstractFileSystem
from fsspec.core import url_to_fs, split_protocol
from appyter.ext.pathlib.chroot import ChrootPurePosixPath

def url_to_chroot_fs(url, pathmap=None, **kwargs):
  ''' Like url_to_fs but supporting our extensions, namely:
  chroot   filesystem path is treated as the root
  pathmap  overlay other fsspec-compatible paths
  '''
  if 'file' not in kwargs: kwargs['file'] = {}
  if 'auto_mkdir' not in kwargs['file']: kwargs['file']['auto_mkdir'] = True
  protocol, path = split_protocol(url)
  full_url = 'chroot::' + (protocol or 'file') + '://' + path
  if pathmap is not None:
    full_url = 'pathmap::' + full_url
    kwargs['pathmap'] = dict(pathmap=pathmap)
  fs, _ = url_to_fs(full_url, **kwargs)
  return fs

class ChrootFileSystem(AbstractFileSystem):
  ''' chroot: update root and disallow access beyond chroot, only works on directories.
  '''
  root_marker = '/'
  protocol = 'chroot'

  def __init__(self, target_protocol=None, target_options=None, fs=None, **kwargs):
    '''
    Parameters
    ----------
    target_protocol: str (optional)
      Target filesystem protocol. Provide either this or ``fs``.
    target_options: dict or None
      Passed to the instantiation of the FS, if fs is None.
    fs: filesystem instance
      The target filesystem to run against. Provide this or ``protocol``.
    '''
    super().__init__(**kwargs)
    if not (fs is None) ^ (target_protocol is None):
      raise ValueError(
          "Please provide one of filesystem instance (fs) or"
          " remote_protocol, not both"
      )
    self.kwargs = target_options or {}
    self.target_protocol = (
      target_protocol
      if isinstance(target_protocol, str)
      else (fs.protocol if isinstance(fs.protocol, str) else fs.protocol[0])
    )
    self.fs = fs if fs is not None else filesystem(target_protocol, **self.kwargs)

  def __resolve_path(self, path):
    return str((ChrootPurePosixPath(self.storage_options['fo']) / path).realpath())

  def __unresolve_path(self, path):
    return '/' + str(PurePosixPath(path).relative_to(self.storage_options['fo']))

  def __enter__(self):
    if getattr(self.fs, '__enter__', None) is not None:
      self.fs.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.fs, '__exit__', None) is not None:
      self.fs.__exit__(type, value, traceback)

  def mkdir(self, path, **kwargs):
    return self.fs.mkdir(self.__resolve_path(path), **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    return self.fs.rm(self.__resolve_path(path), recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    return self.fs.copy(self.__resolve_path(path1), self.__resolve_path(path2), recursive=recursive, on_error=on_error, **kwargs)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    return self.fs.mv(self.__resolve_path(path1), self.__resolve_path(path2), recursive=recursive, maxdepth=maxdepth, **kwargs)

  def info(self, path, **kwargs):
    return self.fs.info(self.__resolve_path(path), **kwargs)

  def ls(self, path, detail=True, **kwargs):
    results = []
    for f in self.fs.ls(self.__resolve_path(path), detail=detail, **kwargs):
      if detail:
        f['name'] = self.__unresolve_path(f['name'])
        results.append(f)
      else:
        results.append(self.__unresolve_path(f))
    return results

  def _open(self, path, mode="rb", block_size=None, cache_options=None, **kwargs):
    return self.fs._open(self.__resolve_path(path), mode=mode, block_size=block_size, cache_options=cache_options, **kwargs)
