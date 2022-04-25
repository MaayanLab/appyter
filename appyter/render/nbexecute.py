import os
import sys
import click
import fsspec
import asyncio
import pathlib
import datetime
import traceback
import logging
logger = logging.getLogger(__name__)

from appyter import __version__
from appyter.cli import cli
from appyter.ext.emitter import json_emitter_factory
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.asyncio.helpers import ensure_async_contextmanager, ensure_sync
from appyter.ext.nbclient import NotebookClientIOPubHook
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io, nb_to_json
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.ext.urllib import URI

def cell_is_code(cell):
    return cell.get('cell_type') == 'code'

def cell_has_error(cell):
    for output in cell['outputs']:
        if output['output_type'] == 'error':
            return True
    return False

def iopub_hook_factory(nb, emit):
  async def iopub_hook(cell, cell_index):
    await emit({ 'type': 'cell', 'data': [cell, cell_index] })
  return iopub_hook

async def nbexecute_async(ipynb='', emit=json_emitter_factory(sys.stdout), cwd='', subscribe=None, fuse=False):
  logger.info('starting')
  assert callable(emit), 'Emit must be callable'
  with fsspec.open(str(URI(cwd).join(ipynb)), 'r') as fr:
    nb = nb_from_ipynb_io(fr)
  #
  if 'appyter' not in nb.metadata:
    logger.warning('detected legacy format, upgrading..')
    nb.metadata['appyter'] = {
      'nbconstruct': {
        'version': 'unknown',
      }
    }
  #
  if 'nbexecute' not in nb.metadata['appyter']:
    nb.metadata['appyter']['nbexecute'] = {
      'version': __version__,
    }
  #
  if 'execution_info' in nb.metadata:
    logger.warning('detected legacy format, upgrading..')
    nb.metadata['appyter']['nbexecute'].update(
      version='unknown',
      started=nb.metadata['execution_info'].get('started'),
      completed=nb.metadata['execution_info'].get('completed'),
    )
    del nb.metadata['execution_info']
  #
  if 'completed' in nb.metadata['appyter']['nbexecute']:
    await emit({ 'type': 'error', 'data': f"Execution already completed at {nb.metadata['appyter']['nbexecute']['completed']}" })
    return
  elif 'started' in nb.metadata['appyter']['nbexecute']:
    await emit({ 'type': 'error', 'data': f"Execution already started at {nb.metadata['appyter']['nbexecute']['started']}" })
    return
  #
  await emit({ 'type': 'status', 'data': 'Starting' })
  state = dict(progress=0, status='Starting')
  #
  try:
    files = nb.metadata['appyter']['nbconstruct'].get('files')
    logger.debug(f"{cwd=} {files=}")
    async with ensure_async_contextmanager(url_to_chroot_fs(cwd, pathmap=files)) as fs:
      async with ensure_async_contextmanager(fs.mount(fuse=fuse)) as mnt:
        # setup execution_info with start time
        nb.metadata['appyter']['nbexecute']['started'] = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
        with (mnt/ipynb).open('w') as fw:
          nb_to_ipynb_io(nb, fw)
        #
        logger.info('initializing')
        if callable(subscribe):
          await subscribe(lambda: dict(nb=nb_to_json(nb), **state))
        #
        try:
          iopub_hook = iopub_hook_factory(nb, emit)
          client = NotebookClientIOPubHook(
            nb,
            allow_errors=True,
            timeout=None,
            kernel_name='python3',
            resources={ 'metadata': {'path': str(mnt) } },
            iopub_hook=iopub_hook,
          )
          await emit({ 'type': 'nb', 'data': nb_to_json(nb) })
          async with client.async_setup_kernel(
            env=dict(
              PYTHONPATH=':'.join(sys.path),
              PATH=os.environ['PATH'],
            ),
          ):
            logger.info('executing')
            state.update(status='Executing...', progress=0)
            await emit({ 'type': 'status', 'data': state['status'] })
            await emit({ 'type': 'progress', 'data': state['progress'] })
            n_cells = len(nb.cells)
            exec_count = 1
            for index, cell in enumerate(nb.cells):
              logger.debug(f"executing cell {index}")
              cell = await client.async_execute_cell(
                cell, index,
                execution_count=exec_count,
              )
              if cell_is_code(cell):
                if cell_has_error(cell):
                  raise Exception('Cell execution error on cell %d' % (exec_count))
                exec_count += 1
              if index < n_cells-1:
                state['progress'] = index + 1
                await emit({ 'type': 'progress', 'data': state['progress'] })
              else:
                state['status'] = 'Success'
                await emit({ 'type': 'status', 'data': state['status'] })
        except asyncio.CancelledError:
          logger.info('cancelled')
          raise
        except Exception as e:
          logger.info(f"execution error: {traceback.format_exc()}")
          await emit({ 'type': 'error', 'data': str(e) })
        # Save execution completion time
        logger.info('saving')
        nb.metadata['appyter']['nbexecute']['completed'] = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
        # save additional files
        # TODO: in the future we should individual files and include the original urls here
        nb.metadata['appyter']['nbexecute']['files'] = {
          path: path
          for path in (
            str(p.relative_to(mnt))
            for p in mnt.rglob('*')
            if p.is_file()
          )
          if path not in (files.keys()|{ipynb})
        }
        #
        with (mnt/ipynb).open('w') as fw:
          nb_to_ipynb_io(nb, fw)
        #
        logger.info('finalized')
  except asyncio.CancelledError:
    logger.info(f"outer cancelled")
    raise
  except Exception as e:
    logger.error(traceback.format_exc())
    if state['status'] != 'Success':
      await emit({ 'type': 'error', 'data': f"Error occured while executing" })
    else:
      await emit({ 'type': 'error', 'data': f"Error occured while finalizing" })
    raise
  finally:
    logger.info('complete')
  #

@cli.command(help='Execute a jupyter notebook on the command line asynchronously')
@click.option('-s', type=str, metavar='URI', default='file:///dev/stdout', help='Status stream')
@click.option('-w', type=str, metavar='DIR', default='storage://', help='Working directory')
@click_option_setenv('--data-dir', envvar='APPYTER_DATA_DIR', default=None, help='The directory that storage:// uris correspond to')
@click_option_setenv('--fuse', envvar='APPYTER_FUSE', default=False, help='Use fuse for execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def nbexecute(ipynb, s=None, w=None, fuse=False, data_dir=None):
  from appyter.ext.emitter import url_to_emitter
  from appyter.ext.asyncio.event_loop import with_event_loop
  from appyter.ext.fsspec.storage import ensure_storage
  if data_dir is None:
    p = pathlib.Path(ipynb)
    data_dir = str(p.parent)
    ipynb = p.name
  with with_event_loop():
    with ensure_sync(url_to_emitter(s)) as emitter:
      with ensure_sync(ensure_storage(data_dir)):
        ensure_sync(nbexecute_async(
          ipynb=ipynb,
          emit=emitter,
          cwd=w,
          fuse=fuse,
        ))
