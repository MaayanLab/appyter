import re
import nbformat as nbf
from copy import deepcopy
from jupyter_template.parse.function_call import FunctionCallMatcher

cell_match = re.compile(r'^(# *)?%%jupyter_template(?P<type>.*?\n)(?P<source>.+)$', re.MULTILINE | re.DOTALL)
template_match = re.compile(r'\{[\{%](?P<inner>.+?)[%\}]\}', re.MULTILINE | re.DOTALL)
field_match = FunctionCallMatcher()

def parse_fields_from_cell(env, cell):
  cell_m = cell_match.match(cell)
  if cell_m:
    cell_source = cell_m.group('source')
    for template_m in template_match.finditer(cell_source):
      for field_m in field_match.finditer(template_m.group('inner')):
        try:
          yield eval(field_m, env.globals)
        except:
          pass

def parse_fields_from_nbtemplate(env, nb):
  return [
    field
    for cell in nb.cells
    for field in parse_fields_from_cell(env, cell['source'])
  ]

def nbtemplate_from_ipynb_string(ipynb):
  return nbf.reads(ipynb, as_version=4)


def nbtemplate_from_ipynb_file(filename):
  return nbf.read(open(filename, 'r'), as_version=4)

