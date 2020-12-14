import os
import json
import click
import nbformat as nbf

from appyter.cli import cli
from appyter.ext.fs import Filesystem
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

@cli.command(help='Inspect appyter for arguments (fields)')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def nbinspect(cwd, ipynb, output, **kwargs):
  env = get_jinja2_env(config=get_env(cwd=cwd, ipynb=ipynb, mode='inspect',  **kwargs))
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  fields = render_nbtemplate_json_from_nbtemplate(env, nbtemplate)
  json.dump(fields, output)
