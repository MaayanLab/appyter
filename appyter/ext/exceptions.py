
def exception_as_dict(exc):
  if getattr(exc, 'as_dict', None) is None:
    return dict(cls=exc.__class__.__name__, message=str(exc))
  else:
    return dict(cls=exc.__class__.__name__, **exc.as_dict())
