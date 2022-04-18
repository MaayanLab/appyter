from fsspec import AbstractFileSystem

class ComposableAbstractFileSystem:
  ''' Expansion of AbstractFileSystem's json serialization methods to support composition
  by calling to_json() on any filesystems in storage_args during serialization,
  and loading them in during deserialization.
  '''
  def to_json(self):
    import json
    cls = type(self)
    cls = '.'.join((cls.__module__, cls.__name__))
    proto = (
      self.protocol[0]
      if isinstance(self.protocol, (tuple, list))
      else self.protocol
    )
    return json.dumps(
      dict(
        **{"cls": cls, "protocol": proto, "args": self.storage_args},
        **{
          k: json.loads(v.to_json()) if isinstance(v, AbstractFileSystem) else v
          for k, v in self.storage_options.items()
        },
      )
    )

  @staticmethod
  def from_json(blob):
    import json
    from fsspec.registry import _import_class, get_filesystem_class
    dic = json.loads(blob)
    protocol = dic.pop("protocol")
    try:
      cls = _import_class(dic.pop("cls"))
    except (ImportError, ValueError, RuntimeError, KeyError, AttributeError):
      cls = get_filesystem_class(protocol)
    if cls.from_json == ComposableAbstractFileSystem.from_json:
      return cls(*dic.pop("args", ()), **{
        k: ComposableAbstractFileSystem.from_json(json.dumps(v)) if type(v) == dict and 'cls' in v else v
        for k, v in dic.items()
      })
    else:
      return cls.from_json(blob)
