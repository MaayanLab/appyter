from fsspec import filesystem, AbstractFileSystem

from pathlib import PurePosixPath

class ChrootPurePosixPath:
  ''' Similar to pathlib but guaranteed to stay within the `root` directory.
  '''
  def __init__(self, root, _path=PurePosixPath('.')):
    self.root = PurePosixPath(root)
    self.path = PurePosixPath(_path)
    assert not self.path.is_absolute()

  def relative_to(self, *other):
    return ChrootPurePosixPath(self.root, self.path.relative_to(*other))

  def realpath(self):
    return self.root / self.path

  def __repr__(self):
    return repr(self.path)

  def __str__(self):
    return str(self.path)

  def __truediv__(self, other):
    path = self.path
    other = PurePosixPath(other)
    parts = other.parts[1:] if other.is_absolute() else other.parts
    for p in parts:
      if p == '..': path = path.parent
      else: path = path / p
    return ChrootPurePosixPath(self.root, path)

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
    pathmap: dict
      A mapping from [path to map onto the target filesystem]: filesystem url to present
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
    return (ChrootPurePosixPath(self.storage_options['fo']) / path).realpath()

  def __unresolve_path(self, path):
    return '/' + str(PurePosixPath(path).relative_to(self.storage_options['fo']))

  def mkdir(self, path, **kwargs):
    return self.fs.mkdir(self.__resolve_path(path), **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    return self.fs.rm(self.__resolve_path(path), recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, **kwargs):
    return self.fs.copy(self.__resolve_path(path1), self.__resolve_path(path2), recursive=recursive, on_error=on_error, **kwargs)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    return self.fs.mv(self.__resolve_path(path1), self.__resolve_path(path2), recursive=recursive, maxdepth=maxdepth, **kwargs)

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
