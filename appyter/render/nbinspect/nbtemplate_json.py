from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

def render_nbtemplate_json_from_nbtemplate(env, nb):
  ''' Render a json representing the relevant Fields throughout the notebook.
  '''
  return [
    { 'field': field.field, 'args': field.args }
    for field in parse_fields_from_nbtemplate(env, nb, deep=True)
  ]
