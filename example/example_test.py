import os, sys; sys.path.insert(0, os.path.realpath('..'))

from appyter.parse.nb import nb_from_ipynb_io
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.form import render_form_from_nbtemplate
from appyter.context import get_jinja2_env, get_env
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.parse.nb import parse_markdown

with open('example.ipynb', 'r') as fr:
  nbtemplate = nb_from_ipynb_io(fr)

config = get_env(cwd=os.path.dirname(__file__), ipynb='example.ipynb')
env = get_jinja2_env(config=config)
parse_fields_from_nbtemplate(env, nbtemplate)

env = get_jinja2_env(config=config)
render_form_from_nbtemplate(env, nbtemplate)

env = get_jinja2_env(
  context={
    'number_1': 8,
    'operator': 'subtract',
  },
  config=config,
)
render_nb_from_nbtemplate(env, nbtemplate)
