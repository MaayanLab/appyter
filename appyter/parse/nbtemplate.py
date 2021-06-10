import re
from appyter.fields import Field, PartialField

cell_match = re.compile(r'^(# *)?%%appyter(?P<type>.*?\n)(?P<source>.+)$', re.MULTILINE | re.DOTALL)

def parse_fields_from_nbtemplate(env, nb, deep=False):
  # catch instanciations of a field into the fields array
  fields = []
  def field_wapper(field):
    def wrapper(**kwargs):
      _field = field(**kwargs)
      fields.append(_field)
      return _field
    return wrapper
  ctx = {
    key: field_wapper(field)
    for key, field in env.globals.items()
    if isinstance(field, Field) or isinstance(field, PartialField)
  }
  # collect jinja2 sources from throughout the entire notebook
  source = '\n'.join(
    cell_m.group('source')
    for cell in nb.cells
    for cell_m in [cell_match.match(cell.source)]
    if cell_m
  )
  # render the source for its side-effect of instantiating
  #  relevant fields, thus populating the fields array
  env.from_string(source).render(ctx)
  if not deep:
    # by convention, fields which accept fields as arguments
    #  will register a `parent` field with their name allowing
    #  us to filter out these sub-fields when necessary
    fields = [
      field
      for field in fields
      if 'parent' not in field['args']
    ]
  return fields
