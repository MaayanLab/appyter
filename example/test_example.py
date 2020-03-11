import os, sys; sys.path.insert(0, os.path.realpath('..'))

from jupyter_template.render.ipynb import render_ipynb_file
from jupyter_template.context import get_jinja2_env

render_ipynb_file(
  get_jinja2_env({
      'number_1': 8,
      'operator': 'subtract',
  }),
  'example.ipynb'
)
