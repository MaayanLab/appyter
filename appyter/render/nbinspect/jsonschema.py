from appyter.util import dict_filter_none
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

def render_jsonschema_from_nbtemplate(env, nb):
  ''' Render a jsonschema representing the relevant Fields throughout the notebook.
  TODO: branch with tabs
  '''
  fields = list(parse_fields_from_nbtemplate(env, nb, deep=True))
  return {
    'type': 'object',
    'properties': dict_filter_none({
      field.args['name']: field.to_jsonschema()
      for field in fields
    }),
    'required': [
      field.args['name']
      for field in fields
      if field.args.get('required')
    ],
  }
