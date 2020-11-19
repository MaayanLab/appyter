import asyncio
import typing as t
from nbclient import NotebookClient
from nbformat import NotebookNode
from nbclient.util import ensure_async
from nbclient.exceptions import CellExecutionComplete, DeadKernelError, CellControlSignal

class NotebookClientIOPubHook(NotebookClient):
  ''' A notebook client with the ability to hook into iopub updates
  '''
  def __init__(self, *args, iopub_hook=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.iopub_hook = iopub_hook

  async def _async_poll_output_msg(
    self,
    parent_msg_id,
    cell,
    cell_index
  ):
    assert self.kc is not None
    complete = False
    while not complete:
      msg = await ensure_async(self.kc.iopub_channel.get_msg(timeout=None))
      if msg['parent_header'].get('msg_id') == parent_msg_id:
        try:
          # Will raise CellExecutionComplete when completed
          self.process_message(msg, cell, cell_index)
        except CellExecutionComplete:
          complete = True
        finally:
          if self.iopub_hook is not None:
            await self.iopub_hook(cell, cell_index)

  def _kc_execute(self, *args, **kwargs):
    try:
      loop = asyncio.get_event_loop()
    except (RuntimeError, AssertionError):
      loop = asyncio.new_event_loop()
      asyncio.set_event_loop(loop)
    return self.kc.execute(*args, **kwargs)

  async def async_execute_cell(
      self,
      cell: NotebookNode,
      cell_index: int,
      execution_count: t.Optional[int] = None,
      store_history: bool = True) -> NotebookNode:
    """
    Executes a single code cell.

    To execute all cells see :meth:`execute`.

    Parameters
    ----------
    cell : nbformat.NotebookNode
      The cell which is currently being processed.
    cell_index : int
      The position of the cell within the notebook object.
    execution_count : int
      The execution count to be assigned to the cell (default: Use kernel response)
    store_history : bool
      Determines if history should be stored in the kernel (default: False).
      Specific to ipython kernels, which can store command histories.

    Returns
    -------
    output : dict
      The execution output payload (or None for no output).

    Raises
    ------
    CellExecutionError
      If execution failed and should raise an exception, this will be raised
      with defaults about the failure.

    Returns
    -------
    cell : NotebookNode
      The cell which was just processed.
    """
    assert self.kc is not None
    if cell.cell_type != 'code' or not cell.source.strip():
      self.log.debug("Skipping non-executing cell %s", cell_index)
      return cell

    if self.record_timing and 'execution' not in cell['metadata']:
      cell['metadata']['execution'] = {}

    self.log.debug("Executing cell:\n%s", cell.source)
    parent_msg_id = await asyncio.get_running_loop().run_in_executor(None,
      lambda: self._kc_execute(
        cell.source,
        store_history=store_history,
        stop_on_error=not self.allow_errors
      )
    )
    # We launched a code cell to execute
    self.code_cells_executed += 1
    exec_timeout = self._get_timeout(cell)

    cell.outputs = []
    self.clear_before_next_output = False

    task_poll_kernel_alive = asyncio.ensure_future(
      self._async_poll_kernel_alive()
    )
    task_poll_output_msg = asyncio.ensure_future(
      self._async_poll_output_msg(parent_msg_id, cell, cell_index)
    )
    self.task_poll_for_reply = asyncio.ensure_future(
      self._async_poll_for_reply(
        parent_msg_id, cell, exec_timeout, task_poll_output_msg, task_poll_kernel_alive
      )
    )
    try:
      exec_reply = await self.task_poll_for_reply
    except asyncio.CancelledError:
      # can only be cancelled by task_poll_kernel_alive when the kernel is dead
      task_poll_output_msg.cancel()
      raise DeadKernelError("Kernel died")
    except Exception as e:
      # Best effort to cancel request if it hasn't been resolved
      try:
        # Check if the task_poll_output is doing the raising for us
        if not isinstance(e, CellControlSignal):
          task_poll_output_msg.cancel()
      finally:
        raise

    if execution_count:
      cell['execution_count'] = execution_count
    self._check_raise_for_error(cell, exec_reply)
    self.nb['cells'][cell_index] = cell
    return cell
