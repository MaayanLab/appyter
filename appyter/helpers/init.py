import os
import re
import sys
import click
import pathlib
from nbformat.v4 import new_code_cell
from appyter.cli import cli
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.ext.click import click_argument_setenv

def slugify(s):
  return re.sub(r'[^a-zA-Z0-9]+', '_', s)

def one_and_only(it):
  try:
    it = iter(it)
    ret = next(it)
    try:
      next(it)
    except StopIteration:
      pass
  except:
    raise
  return ret

@cli.command(help='Scaffold an appyter optionally with an existing Jupyter Notebook')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB', required=False, type=click.Path(file_okay=True, path_type=str))
def init(ipynb, **kwargs):
  if ipynb is not None: ipynb = pathlib.Path(ipynb)
  try:
    from cookiecutter.main import cookiecutter
    if ipynb is None:
      cookiecutter(str(pathlib.Path(__file__).parent / 'cookiecutter'))
    else:
      if (pathlib.Path.cwd() / ipynb.stem).is_dir():
        from cookiecutter.exceptions import OutputDirExistsException
        raise OutputDirExistsException(f"Output directory '{ipynb.stem}' exists")
      cookiecutter(str(pathlib.Path(__file__).parent / 'cookiecutter'),
        extra_context={
          'project_name': ipynb.stem,
        },
      )
      nb = nb_from_ipynb_io(ipynb.open('r'))
      outdir = one_and_only(pathlib.Path.cwd().glob('*/appyter.json')).parent
      project_slug = outdir.name
      if len(nb.cells) == 0 or not nb.cells[0]['source'].startswith('#%%appyter init'):
        nb.cells.insert(0, new_code_cell(
          '#%%appyter init\nfrom appyter import magic\nmagic.init(lambda _=globals: _())'
        ))
      nb_to_ipynb_io(nb, (outdir / ipynb.name).open('w'))
  except ImportError:
    click.echo("Cookiecutter must be installed to use `appyter init`")
    sys.exit(1)
