from pathlib import PurePosixPath

class ChrootPurePosixPath:
  ''' Similar to pathlib but guaranteed to stay within the `root` directory.
  '''
  def __init__(self, root, _path=PurePosixPath('.')):
    self.root = PurePosixPath(root)
    self.path = PurePosixPath(_path)
    assert not self.path.is_absolute()

  def relative_to(self, *other):
    return self.__class__(self.root, self.path.relative_to(*other))

  def realpath(self):
    return self.root / self.path

  def __repr__(self):
    return repr(self.path)

  def __str__(self):
    return str(self.path)

  def join(self, *others):
    path = self.path
    for other in map(PurePosixPath, others):
      parts = other.parts[1:] if other.is_absolute() else other.parts
      for p in parts:
        if p == '..': path = path.parent
        else: path = path / p
    return self.__class__(self.root, path)
    
  def __truediv__(self, other):
    return self.join(other)
