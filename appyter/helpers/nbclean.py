from appyter.cli import cli
from appyter.ext.click import click_argument_setenv
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io

@cli.command(help='Clean an appyters output & metadata to minimize unnecessary data transfers in production')
@click_argument_setenv('ipynb', type=str, envvar='APPYTER_IPYNB')
def nbclean(ipynb, **kwargs):
  nb = nb_from_ipynb_io(open(ipynb, 'r'))
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
  nb_to_ipynb_io(nb, open(ipynb, 'w'))
