import os
import sys
import click
from appyter import __version__
from appyter.cli import cli
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.util import join_routes

@cli.command(
  help='An alias for jupyter notebook which pre-fetches notebook data from a remote appyter and then launches serve',
  context_settings=dict(
    ignore_unknown_options=True,
  ),
)
@click_option_setenv('--data-dir', envvar='APPYTER_DATA_DIR', default=None, help='The directory to store data of executions')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_option_setenv('--host', envvar='APPYTER_HOST', default='0.0.0.0', help='The host to bind to')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this server should run on')
@click.argument('args', nargs=-1, type=click.UNPROCESSED)
@click_argument_setenv('uri', envvar='APPYTER_URI', nargs=1, type=str)
@click.pass_context
def fetch_and_serve(ctx, data_dir, cwd, host, port, args, uri):
  import json
  import tempfile
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
  metadata = nb.get('metadata', {}).get('appyter', {})
  #
  nbconstruct_version = metadata.get('nbconstruct', {}).get('version', 'unknown')
  if nbconstruct_version and nbconstruct_version == __version__:
    pass
  else:
    click.echo(f"WARNING: this appyter was not created with this version, instance version was {nbconstruct_version} and our version is {__version__}. Proceed with caution")
  #
  nbexecute_version = metadata.get('nbexecute', {}).get('version', 'unknown')
  if nbexecute_version and nbexecute_version == __version__:
    pass
  else:
    click.echo(f"WARNING: this appyter was not executed with this version, instance version was {nbexecute_version} and our version is {__version__}. Proceed with caution")
  #
  if 'nbexecute' not in metadata:
    click.echo('WARNING: this appyter instance has not been executed, no results will be available')
  elif 'started' in metadata['nbexecute'] and 'completed' not in metadata['nbexecute']:
    click.echo('WARNING: this appyter is not finished running, no results will be available')
  elif 'started' in metadata['nbexecute'] and 'completed' in metadata['nbexecute']:
    click.echo(f"Appyter ran from {metadata['nbexecute']['started']} to {metadata['nbexecute']['completed']}")
  else:
    click.echo('WARNING: this appyter seems old, this may not work properly, please contact us and we can update it')
  # if tmpdir doesn't exist, create it
  if data_dir is None:
    data_dir = tempfile.mkdtemp()
  # write notebook to data_dir
  os.makedirs(data_dir, exist_ok=True)
  filename = metadata.get('nbconstruct', {}).get('filename', 'appyter.ipynb')
  with open(os.path.join(data_dir, filename), 'w') as fw:
    nbf.write(nb, fw)
  #
  # download all files to data_dir (get files from nbexecute if available otherwise fall back to nbconstruct input-files)
  files = metadata.get('nbexecute', {}).get('files', metadata.get('nbconstruct', {}).get('files', {}))
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
  ctx.invoke(serve, cwd=cwd, data_dir=data_dir, host=host, port=port, args=[*args, filename])
