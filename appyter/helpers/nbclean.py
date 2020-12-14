import os
import click
import nbformat
from appyter.ext.fs import Filesystem
from appyter.cli import cli
from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_argument_setenv

@cli.command(help='Clean an appyters output & metadata to minimize unnecessary data transfers in production')
@click_argument_setenv('ipynb', type=str, envvar='APPYTER_IPYNB')
def nbclean(ipynb, **kwargs):
  nb = nbformat.read(open(ipynb, 'r'), as_version=4)
  for cell in nb.cells:
    if cell['cell_type'] == 'code':
      cell['execution_count'] = None
      cell['metadata'] = {}
      cell['outputs'] = []
    elif cell['cell_type'] == 'markdown':
      if 'outputs' in cell:
        del cell['outputs']
      if 'execution_count' in cell:
        del cell['execution_count']
  if 'widgets' in nb['metadata']:
    del nb['metadata']['widgets']
  nbformat.write(nb, open(ipynb, 'w'))
