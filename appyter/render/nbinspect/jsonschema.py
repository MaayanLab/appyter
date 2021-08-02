import os
import json
import click

from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.ext.fs import Filesystem
from appyter.parse.nb import nb_from_ipynb_io
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.render.nbinspect.cli import nbinspect
from appyter.util import dict_filter_none

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

@nbinspect.command(help='Create JSON Schema for appyter input')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def jsonschema(cwd, ipynb, output, **kwargs):
  cwd = os.path.realpath(cwd)
  env = get_jinja2_env(config=get_env(cwd=cwd, ipynb=ipynb, mode='inspect', **kwargs))
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  json.dump(render_jsonschema_from_nbtemplate(env, nbtemplate), output)
