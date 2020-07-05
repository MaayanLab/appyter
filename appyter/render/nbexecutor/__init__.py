import os
import sys
import functools

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
    emit('cell', [cell, cell_index])
  return iopub_hook

def render_nbexecutor_from_nb(env, nb):
  def nbexecutor(emit=print, session_dir='', cleanup=None, stopper=lambda: False):
    assert callable(emit), 'Emit must be callable'
    try:
      emit('status', 'Starting')
      client = NotebookClientIOPubHook(
        nb,
        allow_errors=True,
        timeout=None,
        kernel_name='python3',
        env=dict(
          PYTHONPATH=':'.join(sys.path),
          PATH=os.environ['PATH'],
        ),
        resources={ 'metadata': {'path': session_dir} },
        iopub_hook=iopub_hook_factory(nb, emit),
      )
      with client.setup_kernel():
        n_cells = len(nb.cells)
        emit('status', 'Executing...')
        emit('progress', 0)
        for index, cell in enumerate(nb.cells):
          assert not stopper(), "Stopper"
          cell = client.execute_cell(
            cell, index,
            execution_count=client.code_cells_executed + 1,
          )
          if cell_is_code(cell):
            if cell_has_error(cell):
              raise Exception('Cell execution error on cell %d' % (index))
          if index < n_cells-1:
            emit('progress', index+1)
          else:
            emit('status', 'Success')
          assert not stopper(), "Stopper"
    except Exception as e:
      print('error', e)
      emit('error', str(e))
    finally:
      if callable(cleanup):
        cleanup(nb)
  return nbexecutor
