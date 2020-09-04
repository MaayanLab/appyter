import os
import sys
import click
import asyncio
import nbformat as nbf
import functools
import datetime
from nbclient.util import ensure_async

from appyter.cli import cli
from appyter.ext.fs import Filesystem
from appyter.ext.nbclient import NotebookClientIOPubHook
from appyter.render.nbviewer import render_nbviewer_from_nb
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io, nb_to_json


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

async def json_emitter(obj):
  import json
  print(json.dumps(obj))

async def nbexecute_async(ipynb='', emit=json_emitter, cwd=''):
  assert callable(emit), 'Emit must be callable'
  fs = Filesystem(cwd)
  with fs.open(ipynb, 'r') as fr:
    nb = nb_from_ipynb_io(fr)
  # early stop if we already have execution_info
  if 'execution_info' in nb.metadata:
    if 'completed' in nb.metadata['execution_info']:
      await emit({ 'type': 'error', 'data': f"Execution already completed at {nb.metadata['execution_info']['completed']}" })
    elif 'started' in nb.metadata['execution_info']:
      await emit({ 'type': 'error', 'data': f"Execution already started at {nb.metadata['execution_info']['started']}" })
    else:
      await emit({ 'type': 'error', 'data': 'Execution already in progress' })
    return
  # setup execution_info with start time
  nb.metadata['execution_info'] = {
    'started': datetime.datetime.now().replace(
      tzinfo=datetime.timezone.utc
    ).isoformat()
  }
  with fs.open(ipynb, 'w') as fw:
    nb_to_ipynb_io(nb, fw)
  with Filesystem('tmpfs://') as tmp_fs:
    try:
      await emit({ 'type': 'status', 'data': 'Starting' })
      iopub_hook = iopub_hook_factory(nb, emit)
      client = NotebookClientIOPubHook(
        nb,
        allow_errors=True,
        timeout=None,
        kernel_name='python3',
        env=dict(
          PYTHONPATH=':'.join(sys.path),
          PATH=os.environ['PATH'],
        ),
        resources={ 'metadata': {'path': tmp_fs.path()} },
        iopub_hook=iopub_hook,
      )
      await emit({ 'type': 'nb', 'data': nb_to_json(nb) })
      async with client.async_setup_kernel():
        # monkey-patch open so that writes go to s3
        # WARNING: In the case of error with this cell, things proceed anyway
        await ensure_async(
          client.kc.execute(
            '\n'.join([
              f"from appyter.ext.fs import Filesystem as _Filesystem",
              f"open = _Filesystem({repr(cwd)}).open",
            ]),
            store_history=False,
          )
        )
        await emit({ 'type': 'status', 'data': 'Executing...' })
        await emit({ 'type': 'progress', 'data': 0 })
        n_cells = len(nb.cells)
        exec_count = 1
        for index, cell in enumerate(nb.cells):
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
            await emit({ 'type': 'progress', 'data': index })
          else:
            await emit({ 'type': 'status', 'data': 'Success' })
    except Exception as e:
      await emit({ 'type': 'error', 'data': str(e) })
    # Save execution completion time
    nb.metadata['execution_info']['completed'] = datetime.datetime.now().replace(
      tzinfo=datetime.timezone.utc
    ).isoformat()
    #
    with fs.open(ipynb, 'w') as fw:
      nb_to_ipynb_io(nb, fw)

@cli.command(help='Execute a jupyter notebook on the command line asynchronously')
@click.option('--cwd', envvar='CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click.argument('ipynb', envvar='IPYNB')
def nbexecute(ipynb, emit, cwd):
  import asyncio
  loop = asyncio.get_event_loop()
  loop.run_until_complete(nbexecute_async(ipynb, emit, cwd))
  loop.close()
