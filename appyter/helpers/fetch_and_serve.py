import os
import sys
import click
from appyter import __version__
from appyter.cli import cli
from appyter.util import click_option_setenv, click_argument_setenv, join_routes

@cli.command(
  help='An alias for jupyter notebook which pre-fetches notebook data from a remote appyter and then launches serve',
  context_settings=dict(
    ignore_unknown_options=True,
  ),
)
@click_option_setenv('--data-dir', envvar='APPYTER_DATA_DIR', default='data', help='The directory to store data of executions')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this flask server should run on')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click_argument_setenv('uri', envvar='APPYTER_URI', nargs=1, type=str)
@click.pass_context
def fetch_and_serve(ctx, data_dir, cwd, port, args, uri):
  import json
  import urllib.request
  import nbformat as nbf
  # fetch the actual notebook
  try:
    with urllib.request.urlopen(
      urllib.request.Request(uri, headers={ 'Accept': 'application/vnd.jupyter' })
    ) as fr:
      nb = nbf.read(fr, as_version=4)
  except:
    import traceback
    traceback.print_exc()
    click.echo('Error fetching appyter instance, is the url right?')
  #
  metadata = nb.get('metadata', {})
  #
  version = metadata.get('appyter_version')
  if version and version == __version__:
    pass
  else:
    click.echo(f"WARNING: this appyter was not created with this version, instance version was {version} and our version is {__version__}. Proceed with caution")
  #
  execution_info = metadata.get('execution_info', {})
  if not execution_info:
    click.echo('WARNING: this appyter instance has not been executed, no results will be available')
  elif execution_info.get('started') and not execution_info.get('completed'):
    click.echo('WARNING: this appyter is not finished running, no results will be available')
  elif execution_info.get('started') and execution_info.get('completed'):
    click.echo(f"Appyter ran from {execution_info['started']} to {execution_info['completed']}")
  else:
    click.echo('WARNING: this appyter seems old, this may not work properly, please contact us and we can update it')
  #
  # write notebook to data_dir
  os.makedirs(data_dir, exist_ok=True)
  filename = metadata.get('filename', 'appyter.ipynb')
  with open(os.path.join(data_dir, filename), 'w') as fw:
    nbf.write(nb, fw)
  #
  # download all files to data_dir
  files = metadata.get('files', {})
  for file, fileurl in files.items():
    # relative file paths (those without schemes) are relative to the base uri
    # TODO: in the future we might be able to mount these paths as we do in the job
    if '://' not in fileurl:
      fileurl = join_routes(uri, fileurl)[1:]
    click.echo(f"Fetching {file} from {fileurl}...")
    urllib.request.urlretrieve(fileurl, os.path.join(data_dir, file))
  #
  click.echo(f"Done. Starting `appyter serve`...")
  # serve the bundle in jupyter notebook
  from appyter.helpers.serve import serve
  ctx.invoke(serve, cwd=cwd, data_dir=data_dir, port=port, args=[*args, filename])
