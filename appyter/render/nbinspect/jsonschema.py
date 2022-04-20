import os
import json
import click
import fsspec

from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.ext.urllib import join_slash
from appyter.parse.nb import nb_from_ipynb_io
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.render.nbinspect.cli import nbinspect
from appyter.ext.dict import dict_filter_none

def render_jsonschema_from_nbtemplate(env, nb):
  ''' Render a jsonschema representing the relevant Fields throughout the notebook.
  TODO: branch with tabs
  '''
  fields = list(parse_fields_from_nbtemplate(env, nb, deep=True))
  schema = {
    'type': 'object',
    'properties': dict_filter_none({
      field.args['name']: field.to_jsonschema()
      for field in fields
    }),
  }
  required = [
    field.args['name']
    for field in fields
    if field.args.get('required')
  ]
  if required: schema['required'] = required
  return schema

@nbinspect.command(help='Create JSON Schema for appyter input')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def jsonschema(cwd, ipynb, output, **kwargs):
  cwd = os.path.realpath(cwd)
  env = get_jinja2_env(config=get_env(cwd=cwd, ipynb=ipynb, mode='inspect', **kwargs))
  with fsspec.open(join_slash(cwd, ipynb), 'r') as fr:
    nbtemplate = nb_from_ipynb_io(fr)
  json.dump(render_jsonschema_from_nbtemplate(env, nbtemplate), output)
