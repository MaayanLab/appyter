import nbformat as nbf
from jupyter_template.parse.nbtemplate import parse_fields


def get_fields_from_nb(env, nb):
  return [
    field
    for cell in nb.cells
    for field in parse_fields(
      cell['source'],
      env.globals,
    )
  ]


def render_form(env, nb):
  return env.get_template('form.j2').render(
    _fields=get_fields_from_nb(env, nb)
  )


def render_form_from_ipynb(env, ipynb):
  return render_form(
    env,
    nbf.reads(ipynb, as_version=4)
  )


def render_form_from_ipynb_file(env, filename):
  return render_form(
    env,
    nbf.read(open(filename, 'r'), as_version=4)
  )
