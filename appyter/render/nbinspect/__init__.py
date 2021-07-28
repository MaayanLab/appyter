import os
import json
import click
import fsspec

from appyter.cli import cli
from appyter.ext.urllib import join_url
from appyter.util import dict_filter_none
from appyter.parse.nb import nb_from_ipynb_io
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_option_setenv, click_argument_setenv

def render_nbtemplate_json_from_nbtemplate(env, nb):
  ''' Render a json representing the relevant Fields throughout the notebook.
  '''
  return [
    { 'field': field.field, 'args': field.args }
    for field in parse_fields_from_nbtemplate(env, nb, deep=True)
  ]

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

@cli.command(help='Inspect appyter for arguments (fields)')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click.option('-f', '--format', default='appyter', type=click.Choice(['appyter', 'jsonschema'], case_sensitive=False), help='The format of the inspect results')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def nbinspect(cwd, ipynb, output, format='appyter', **kwargs):
  env = get_jinja2_env(config=get_env(cwd=cwd, ipynb=ipynb, mode='inspect',  **kwargs))
  with fsspec.open(join_url(cwd, ipynb), 'r') as fr:
    nbtemplate = nb_from_ipynb_io(fr)
  fields = render_nbtemplate_json_from_nbtemplate(env, nbtemplate)
  if format == 'appyter':
    json.dump(render_nbtemplate_json_from_nbtemplate(env, nbtemplate), output)
  elif format == 'jsonschema':
    json.dump(render_jsonschema_from_nbtemplate(env, nbtemplate), output)
  else:
    raise NotImplementedError
