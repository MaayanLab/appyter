import fsspec
from appyter.ext.fsspec.chroot import ChrootFileSystem

_singletons = {}

class SingletonFileSystem(ChrootFileSystem):
  ''' Instantiation of a singleton filesystem will register it by protocol after which
  the protocol can be used to re-instantiate the singleton instance. Serialization
  works for this enabling the singleton to re-register itself across process boundaries.
  '''
  root_marker = ''

  def __init__(self, proto=None, fs=None, **kwargs):
    global _singletons
    if proto is None:
      if self.__class__.protocol == 'chroot':
        raise ValueError('proto is required')
      proto = self.__class__.protocol
    if fs is None:
      fs = _singletons[proto]
    super(SingletonFileSystem, self).__init__(fs=fs, **kwargs)
    if proto not in _singletons:
      _singletons[proto] = self
      class SingletonFileSystem_(SingletonFileSystem):
        protocol = proto
        def to_json(self):
          global _singletons
          return _singletons[proto].to_json()
      SingletonFileSystem_.__name__ = 'SingletonFileSystem'
      fsspec.register_implementation(proto, SingletonFileSystem_)
    self.protocol = proto
    self.stack_count = 0
  
  def __enter__(self):
    if not self.stack_count:
      super(SingletonFileSystem, self).__enter__()
    self.stack_count += 1
    return self

  def __exit__(self, type, value, traceback):
    self.stack_count -= 1
    if not self.stack_count:
      super(SingletonFileSystem, self).__exit__(type, value, traceback)
