import os
import sys
import click
from appyter.cli import cli
from appyter.util import click_option_setenv

@cli.command(
  help='A simple alias for jupyter notebook which re-uses appyter environment config',
  context_settings=dict(
    ignore_unknown_options=True,
  ),
)
@click_option_setenv('--data-dir', envvar='APPYTER_DATA_DIR', default='data', help='The directory to store data of executions')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this flask server should run on')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def serve(data_dir, cwd, port, args):
  from subprocess import Popen
  # add cwd (the appyter itself) to the PYTHONPATH
  sys.path.insert(0, os.path.realpath(cwd))
  # but use data_dir (the appyter files) as the cwd of the jupyter notebook
  os.makedirs(data_dir, exist_ok=True)
  # run jupyter notebook interactively and exit with it
  proc = Popen(
    ['jupyter', 'notebook', f"--NotebookApp.port={port}", *args],
    stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr,
    cwd=os.path.realpath(data_dir),
    env=dict(
      PYTHONPATH=':'.join(sys.path),
      PATH=os.environ['PATH']
    ),
  )
  exit_code = None
  while exit_code is None:
    try:
      exit_code = proc.wait()
    except:
      pass
    #
  sys.exit(exit_code)
