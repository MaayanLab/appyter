def re_full(expr):
  if not expr.startswith('^'): expr = '^' + expr
  if not expr.endswith('$'): expr = expr + '$'
  return expr

def slugify(s):
  import re
  return re.sub(r'[^a-zA-Z0-9]+', '_', s)
