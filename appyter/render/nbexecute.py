import os
import sys
import click
import asyncio
import nbformat as nbf
import functools
import datetime
import traceback
import logging
logger = logging.getLogger(__name__)

from appyter import __version__
from appyter.cli import cli
from appyter.ext.fs import Filesystem
from appyter.ext.nbclient import NotebookClientIOPubHook
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io, nb_to_json
from appyter.ext.click import click_option_setenv, click_argument_setenv

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

def json_emitter_factory(output):
  async def json_emitter(obj):
    import json
    print(json.dumps(obj), file=output)
  return json_emitter

async def nbexecute_async(ipynb='', emit=json_emitter_factory(sys.stdout), cwd='', subscribe=None):
  logger.info('nbexecute starting')
  assert callable(emit), 'Emit must be callable'
  with Filesystem(cwd, asynchronous=True) as fs:
    with fs.open(ipynb, 'r') as fr:
      nb = nb_from_ipynb_io(fr)
  #
  if 'appyter' not in nb.metadata:
    logger.warn('detected legacy format, upgrading..')
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
    logger.warn('detected legacy format, upgrading..')
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
  #
  try:
    with Filesystem(cwd, with_path=True, asynchronous=True) as fs:
      # setup execution_info with start time
      nb.metadata['appyter']['nbexecute']['started'] = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
      with fs.open(ipynb, 'w') as fw:
        nb_to_ipynb_io(nb, fw)
      #
      logger.info('nbexecute initializing')
      state = dict(progress=0, status='Starting')
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
          resources={ 'metadata': {'path': fs.path()} },
          iopub_hook=iopub_hook,
        )
        await emit({ 'type': 'nb', 'data': nb_to_json(nb) })
        async with client.async_setup_kernel(
          env=dict(
            PYTHONPATH=':'.join(sys.path),
            PATH=os.environ['PATH'],
          ),
        ):
          logger.info('nbexecute executing')
          state.update(status='Executing...', progress=0)
          await emit({ 'type': 'status', 'data': state['status'] })
          await emit({ 'type': 'progress', 'data': state['progress'] })
          n_cells = len(nb.cells)
          exec_count = 1
          for index, cell in enumerate(nb.cells):
            logger.info(f"nbexecute executing cell {index}")
            cell = await client.async_execute_cell(
              cell, index,
              execution_count=exec_count,
            )
            await iopub_hook(cell, index)
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
        raise
      except Exception as e:
        logger.info(f"nbexecute execution error")
        await emit({ 'type': 'error', 'data': str(e) })
      # Save execution completion time
      logger.info('nbexecute saving')
      nb.metadata['appyter']['nbexecute']['completed'] = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc).isoformat()
      # save additional files
      # TODO: in the future we should individual files and include the original urls here
      nb.metadata['appyter']['nbexecute']['files'] = {
        path: path
        for path in fs.ls()
        if path != ipynb
      }
      #
      with fs.open(ipynb, 'w') as fw:
        nb_to_ipynb_io(nb, fw)
      #
  except asyncio.CancelledError:
    raise
  except Exception as e:
    await emit({ 'type': 'status', 'data': 'Error initializing, try again later' })
    logger.error(traceback.format_exc())
  finally:
    logger.info('nbexecute complete')
  #

@cli.command(help='Execute a jupyter notebook on the command line asynchronously')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location to write dynamic updates')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def nbexecute(ipynb, output, cwd):
  import asyncio
  loop = asyncio.get_event_loop()
  loop.run_until_complete(nbexecute_async(ipynb=ipynb, emit=json_emitter_factory(output), cwd=cwd))
  loop.close()
