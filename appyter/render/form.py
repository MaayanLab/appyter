from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

def render_form_from_nbtemplate(env, nb):
  ''' Render a form with the Fields requested throughout the notebook.
  `form.j2` is responsible for calling render on each relevant field.
  '''
  return env.get_template('form.j2').render(
    _fields=parse_fields_from_nbtemplate(env, nb)
  )
