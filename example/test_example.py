import os, sys; sys.path.insert(0, os.path.realpath('..'))

from appyter.parse.nbtemplate import nbtemplate_from_ipynb_file
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.form import render_form_from_nbtemplate
from appyter.context import get_jinja2_env
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

nbtemplate = nbtemplate_from_ipynb_file('example.ipynb')

env = get_jinja2_env()
parse_fields_from_nbtemplate(env, nbtemplate)

env = get_jinja2_env()
render_form_from_nbtemplate(env, nbtemplate)

env = get_jinja2_env({
  'number_1': 8,
  'operator': 'subtract',
})
render_nb_from_nbtemplate(env, nbtemplate)
