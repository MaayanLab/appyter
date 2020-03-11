from jupyter_template.parse.nbtemplate import parse_fields_from_nbtemplate

def render_form_from_nbtemplate(env, nb):
  return env.get_template('form.j2').render(
    _fields=parse_fields_from_nbtemplate(env, nb)
  )
