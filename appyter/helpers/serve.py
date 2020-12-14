import os
import sys
import click
from appyter.cli import cli
from appyter.ext.click import click_option_setenv

@cli.command(
  help='A simple alias for jupyter notebook which re-uses appyter environment config',
  context_settings=dict(
    ignore_unknown_options=True,
  ),
)
@click_option_setenv('--data-dir', envvar='APPYTER_DATA_DIR', default=None, help='The directory to store data of executions')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_option_setenv('--host', envvar='APPYTER_HOST', default='0.0.0.0', help='The host to bind to')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this server should run on')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
def serve(data_dir, cwd, host, port, args):
  import tempfile
  from subprocess import Popen
  # add cwd (the appyter itself) to the PYTHONPATH
  sys.path.insert(0, os.path.realpath(cwd))
  # create blank data_dir as tmpdir if it doesn't exist
  if data_dir is None:
    data_dir = tempfile.mkdtemp()
  #
  # but use data_dir (the appyter files) as the cwd of the jupyter notebook
  os.makedirs(data_dir, exist_ok=True)
  #
  # prepare default flags
  flags = {
    'NotebookApp.ip': host,
    'NotebookApp.port': port,
    'NotebookApp.token': '',
    'NotebookApp.password': '',
  }
  # look through args and replace any overrides
  extra_args = []
  for arg in args:
    if arg.startswith('--'):
      name, value = arg[2:].split('=', maxsplit=1)
      flags[name] = value
    else:
      extra_args.append(arg)
  #
  # run jupyter notebook interactively and exit with it
  proc = Popen(
    [
      'jupyter', 'notebook',
      *[
        f"--{key}={value}"
        for key, value in flags.items()
      ],
      *extra_args,
    ],
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
