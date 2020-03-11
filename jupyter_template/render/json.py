import json
from jupyter_template.parse.nbtemplate import parse_fields_from_nbtemplate

def render_nbtemplate_json_from_nbtemplate(env, nb):
  ''' Render a json representing the relevant Fields throughout the notebook.
  '''
  return json.dumps([
    field.args
    for field in parse_fields_from_nbtemplate(env, nb)
  ])
