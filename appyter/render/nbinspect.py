import os
import json
import click
import nbformat as nbf

from appyter.cli import cli
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.context import get_env, get_jinja2_env

def render_nbtemplate_json_from_nbtemplate(env, nb):
  ''' Render a json representing the relevant Fields throughout the notebook.
  '''
  return [
    { 'field': field.field, 'args': field.args }
    for field in parse_fields_from_nbtemplate(env, nb)
  ]

@cli.command(help='Inspect appyter for arguments (fields)')
@click.option('--output', envvar='OUTPUT', default='-', type=click.File('w'), help='The output location of the inspection json')
@click.option('--cwd', envvar='CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click.argument('ipynb', envvar='IPYNB')
def nbinspect(cwd, ipynb, output, **kwargs):
  env = get_jinja2_env(get_env(cwd=cwd, ipynb=ipynb, **kwargs))
  nbtemplate = nbf.read(open(os.path.join(cwd, ipynb), 'r'), as_version=4)
  fields = render_nbtemplate_json_from_nbtemplate(env, nbtemplate)
  json.dump(fields, output)
