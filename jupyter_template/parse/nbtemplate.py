import re
from jupyter_template.parse.function_call import FunctionCallMatcher

cell_match = re.compile(r'^(# *)?%%jupyter_template(?P<type>.*?\n)(?P<source>.+)$', re.MULTILINE | re.DOTALL)
template_match = re.compile(r'\{[\{%](?P<inner>.+?)[%\}]\}', re.MULTILINE | re.DOTALL)
field_match = FunctionCallMatcher()

def parse_fields(cell, context):
  cell_m = cell_match.match(cell)
  if cell_m:
    cell_source = cell_m.group('source')
    for template_m in template_match.finditer(cell_source):
      for field_m in field_match.finditer(template_m.group('inner')):
        try:
          yield eval(field_m, context)
        except:
          pass
