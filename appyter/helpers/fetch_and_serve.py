import os
import click
import logging
from appyter import __version__
from appyter.cli import cli
from appyter.ext.click import click_option_setenv, click_argument_setenv

logger = logging.getLogger(__name__)

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
  import urllib.parse, urllib.request
  import fsspec
  # TODO: can this be less reliant on the `appyter-catalog` storage setup
  uri_parsed = urllib.parse.urlparse(uri)
  from appyter.ext.fsspec.storage import ensure_storage
  from appyter.ext.asyncio.helpers import ensure_sync_contextmanager
  from appyter.ext.fsspec.core import url_to_chroot_fs
  with ensure_sync_contextmanager(ensure_storage(f"{uri_parsed.scheme}://{uri_parsed.netloc}/storage/appyters/")):
    # if data_dir doesn't exist, create it
    if data_dir is None: data_dir = 'memory://'
    # mount the appyter into the data_dir
    fs = url_to_chroot_fs(data_dir, appyter=uri)
    with fs.mount(fuse=False) as mnt:
      logging.info(f"Starting `appyter serve`...")
      # serve the bundle in jupyter notebook
      from appyter.helpers.serve import serve
      ctx.invoke(serve, cwd=cwd, data_dir=str(mnt), host=host, port=port, args=args)
