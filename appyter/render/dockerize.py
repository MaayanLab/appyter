import os
import click
from appyter.ext.fs import Filesystem
from appyter.cli import cli
from appyter.context import get_env, get_jinja2_env

@cli.command(help='Dockerize an appyter for maximum reproducibility')
@click.option('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click.option('--output', envvar='APPYTER_OUTPUT', default='-', type=click.File('w'), help='The output location of the serialized dockerfile')
@click.argument('ipynb', envvar='APPYTER_IPYNB')
def dockerize(ipynb, cwd, output, **kwargs):
  env = get_jinja2_env(
    config=get_env(cwd=cwd, ipynb=ipynb, mode='dockerize', **kwargs),
  )
  env.get_template('production/Dockerfile.j2').stream().dump(output)
