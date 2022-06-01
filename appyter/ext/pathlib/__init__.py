def is_relative_to(p, *other):
  ''' Re-impl of PurePosixPath.is_relative_to for older python versions
  '''
  try:
    p.relative_to(*other)
    return True
  except ValueError:
    return False