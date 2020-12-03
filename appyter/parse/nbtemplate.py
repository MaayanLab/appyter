import re
from appyter.fields import Field
from appyter.parse.function_call import FunctionCallMatcher

cell_match = re.compile(r'^(# *)?%%appyter(?P<type>.*?\n)(?P<source>.+)$', re.MULTILINE | re.DOTALL)
template_match = re.compile(r'\{[\{%](?P<inner>.+?)[%\}]\}', re.MULTILINE | re.DOTALL)
field_match = FunctionCallMatcher()

def parse_fields_from_cell(env, cell, deep=False):
  cell_m = cell_match.match(cell.source)
  if cell_m:
    cell_source = cell_m.group('source')
    for template_m in template_match.finditer(cell_source):
      for field_m in field_match.finditer(template_m.group('inner'), deep=deep):
        try:
          result = eval(field_m, env.globals)
          if isinstance(result, Field):
            yield result
        except:
          pass

def parse_fields_from_nbtemplate(env, nb, deep=False):
  return [
    field
    for cell in nb.cells
    for field in parse_fields_from_cell(env, cell, deep=deep)
  ]
