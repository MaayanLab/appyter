
def re_full(expr):
  if not expr.startswith('^'): expr = '^' + expr
  if not expr.endswith('$'): expr = expr + '$'
  return expr
