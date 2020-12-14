import os
import json
import click
import nbformat as nbf
from copy import deepcopy

from appyter import __version__
from appyter.cli import cli
from appyter.ext.fs import Filesystem
from appyter.context import get_env, get_jinja2_env
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.parse.nbtemplate import cell_match
from appyter.ext.click import click_option_setenv, click_argument_setenv

def render_cell(env, cell):
  ''' Render a single cell, calling jinja2 templates when necessary
  (only on %%appyter -matched cells) and converting cells
  to markdown / removing them as necessary.
  '''
  if cell.cell_type == 'code':
    cell.outputs = []
    cell['execution_count'] = None

  cell_m = cell_match.match(cell.source)
  if cell_m:
    cell_type = cell_m.group('type').strip().split('_')
    cell_source = cell_m.group('source').strip()

    if cell_type == ['init']:
      return None

    template = env.from_string(cell_source)
    rendered = template.render()
    trimmed = '\n'.join(
      line
      for line in rendered.splitlines()
      if line.strip() != ''
    )

    # Variables added via jinja should get added to globals
    #  for subsequent evaluation
    for k, v in template.module.__dict__.items():
      if not k.startswith('_'):
        env.globals[k] = v

    # Alter cell render based on cell_type
    if cell_type == ['markdown']:
      cell = nbf.v4.new_markdown_cell(rendered)
    elif 'hide' in cell_type or not trimmed:
      cell = None
    else:
      cell = nbf.v4.new_code_cell(trimmed)

  return cell


def render_nb_from_nbtemplate(env, nb, files={}):
  ''' Render the notebook by rendering the jinja2 templates using the context in env.
  '''
  nb = deepcopy(nb)
  nb.cells = list(filter(None, [
    render_cell(
      env,
      cell,
    )
    for cell in nb.cells
  ]))
  if 'appyter' not in nb.metadata:
    nb.metadata['appyter'] = {}
  nb.metadata['appyter']['nbconstruct'] = dict(
    version=__version__,
    filename=env.globals['_config']['IPYNB'],
    files=files,
  )
  return nb

@cli.command(help='Construct jupyter notebook from appyter and arguments')
@click.option('-i', '--context', envvar='APPYTER_CONTEXT', default='-', type=click.File('r'), help='JSON serialized context mapping field names to values')
@click.option('-o', '--output', envvar='APPYTER_OUTPUT', default='-', type=click.File('w'), help='The output location of the serialized jupyter notebook')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def nbconstruct(cwd, ipynb, context, output, **kwargs):
  context = json.load(context)
  env = get_jinja2_env(
    config=get_env(cwd=cwd, ipynb=ipynb, mode='construct', **kwargs),
    context=context,
  )
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  nb_to_ipynb_io(nb, output)
