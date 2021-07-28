import os
import json
import click
import fsspec

from appyter.cli import cli
from appyter.ext.urllib import join_url
from appyter.util import dict_filter_none
from appyter.parse.nb import nb_from_ipynb_io
from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_option_setenv, click_argument_setenv

from appyter.render.nbinspect.nbtemplate_json import render_nbtemplate_json_from_nbtemplate
from appyter.render.nbinspect.jsonschema import render_jsonschema_from_nbtemplate
from appyter.render.nbinspect.cwl import render_cwl_from_nbtemplate

@cli.command(help='Inspect appyter for arguments (fields)')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click.option('-f', '--format', default='appyter', type=click.Choice(['appyter', 'jsonschema', 'cwl'], case_sensitive=False), help='The format of the inspect results')
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
  elif format == 'cwl':
    json.dump(render_cwl_from_nbtemplate(env, nbtemplate, cwd=cwd, ipynb=ipynb), output)
  else:
    raise NotImplementedError
