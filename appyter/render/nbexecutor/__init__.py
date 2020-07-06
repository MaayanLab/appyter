import os
import sys
import click
import nbformat as nbf
import functools

from appyter.cli import cli
from appyter.ext.nbclient import NotebookClientIOPubHook
from appyter.render.nbviewer import render_nbviewer_from_nb


def cell_is_code(cell):
    return cell.get('cell_type') == 'code'

def cell_has_error(cell):
    for output in cell['outputs']:
        if output['output_type'] == 'error':
            return True
    return False

def iopub_hook_factory(nb, emit):
  def iopub_hook(cell, cell_index):
    emit({ 'type': 'cell', 'data': [cell, cell_index] })
  return iopub_hook

def json_emitter(obj):
  import json
  print(json.dumps(obj))

@cli.command(help='Execute a jupyter notebook on the command line asynchronously')
@click.option('--cwd', envvar='CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click.argument('ipynb', envvar='IPYNB')
def nbexecutor(ipynb='', emit=json_emitter, cwd=''):
  assert callable(emit), 'Emit must be callable'
  with open(os.path.join(cwd, ipynb), 'r') as fr:
    nb = nbf.read(fr, as_version=4)
  try:
    emit({ 'type': 'status', 'data': 'Starting' })
    client = NotebookClientIOPubHook(
      nb,
      allow_errors=True,
      timeout=None,
      kernel_name='python3',
      env=dict(
        PYTHONPATH=':'.join(sys.path),
        PATH=os.environ['PATH'],
      ),
      resources={ 'metadata': {'path': cwd} },
      iopub_hook=iopub_hook_factory(nb, emit),
    )
    with client.setup_kernel():
      n_cells = len(nb.cells)
      emit({ 'type': 'status', 'data': 'Executing...' })
      emit({ 'type': 'progress', 'data': 0 })
      for index, cell in enumerate(nb.cells):
        cell = client.execute_cell(
          cell, index,
          execution_count=client.code_cells_executed + 1,
        )
        if cell_is_code(cell):
          if cell_has_error(cell):
            raise Exception('Cell execution error on cell %d' % (index))
        if index < n_cells-1:
          emit({ 'type': 'progress', 'data': index+1 })
        else:
          emit({ 'type': 'status', 'data': 'Success' })
  except Exception as e:
    emit({ 'type': 'error', 'data': str(e) })
  #
  with open(os.path.join(cwd, ipynb), 'w') as fw:
    nbf.write(nb, fw)
