from appyter.render.nbviewer import render_nbviewer_from_nb
from appyter.render.nbexecutor.yielding_preprocessor import YieldingExecutePreprocessor

def cell_is_code(cell):
    return cell.get('cell_type') == 'code'

def cell_has_error(cell):
    for output in cell['outputs']:
        if output['output_type'] == 'error':
            return True
    return False

def render_nbexecutor_from_nb(env, nb):
  def nbexecutor(emit=print, session_dir='', cleanup=None, stopper=lambda: False):
    assert callable(emit), 'Emit must be callable'
    try:
      emit('status', 'Starting')
      yep = YieldingExecutePreprocessor(
        allow_errors=True,
        timeout=None,
        kernel_name='python3',
      )
      resources = {'metadata': {'path': session_dir} }
      index = 0
      code_cell_index = 0
      n_cells = len(nb.cells)
      emit('status', 'Executing...')
      emit('progress', index)
      for cell, _ in yep.preprocess(nb, resources):
        assert not stopper(), "Stopper"
        emit('cell', cell)
        if cell_is_code(cell):
          code_cell_index += 1
          if cell_has_error(cell):
            raise Exception('Cell execution error on cell %d' % (code_cell_index))
        index += 1
        if index < n_cells:
          emit('progress', index)
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
