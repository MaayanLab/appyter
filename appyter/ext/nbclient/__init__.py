import asyncio
import typing as t
from contextlib import asynccontextmanager
from nbclient import NotebookClient
from nbformat import NotebookNode
from nbclient.exceptions import CellExecutionComplete, DeadKernelError, CellControlSignal
from nbclient.util import run_hook
from nbclient.client import timestamp
from appyter.ext.asyncio.event_loop import get_event_loop
from appyter.ext.asyncio.helpers import ensure_async

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
    ''' Override output_msg polling to send to iopub_hook
    '''
    assert self.kc is not None
    complete = False
    while not complete:
      msg = await ensure_async(self.kc.iopub_channel.get_msg(timeout=None))
      if msg['parent_header'].get('msg_id') == parent_msg_id:
        try:
          # Will raise CellExecutionComplete when completed
          await self.process_message(msg, cell, cell_index)
        except CellExecutionComplete:
          complete = True
        finally:
          if self.iopub_hook is not None:
            await self.iopub_hook(cell, cell_index)

  async def handle_comm_msg(
    self,
    outs: t.List,
    msg: t.Dict,
    cell_index: int
  ) -> None:
    ''' Store ipywidget state in each cell during execution and trigger iopub_hook
    '''
    super().handle_comm_msg(outs, msg, cell_index)
    content = msg['content']
    data = content['data']
    if self.store_widget_state and 'state' in data:  # ignore custom msg'es
      # Here we store the updated state in the cell during execution, and trigger an iopub_hook
      # we'll arbitrarily choose to store it in the cell's metadata.widget-state
      cell = self.nb['cells'][cell_index]
      cell.setdefault('metadata', {}).setdefault('widgets', {
        'version_major': 2,
        'version_minor': 0,
      }).setdefault('state', {}).update({
        content['comm_id']: self._serialize_widget_state(self.widget_state[content['comm_id']]),
      })
      for key, widget in cell['metadata']['widgets']['state'].items():
        buffers = self.widget_buffers.get(key)
        if buffers:
            widget['buffers'] = buffers
      if self.iopub_hook is not None:
        await self.iopub_hook(cell, cell_index)

  def _kc_execute(self, *args, **kwargs):
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
    parent_msg_id = await ensure_async(self._kc_execute)(
      cell.source,
      store_history=store_history,
      stop_on_error=not self.allow_errors
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
    await self._check_raise_for_error(cell, cell_index, exec_reply)
    self.nb['cells'][cell_index] = cell
    return cell

  @asynccontextmanager
  async def async_setup_kernel(self, **kwargs) -> t.AsyncGenerator:
      """
      Context manager for setting up the kernel to execute a notebook.

      This assigns the Kernel Manager (``self.km``) if missing and Kernel Client(``self.kc``).

      When control returns from the yield it stops the client's zmq channels, and shuts
      down the kernel.
      """
      # by default, cleanup the kernel client if we own the kernel manager
      # and keep it alive if we don't
      cleanup_kc = kwargs.pop('cleanup_kc', self.owns_km)
      if self.km is None:
          self.km = self.create_kernel_manager()

      loop = get_event_loop()

      if not self.km.has_kernel:
          await self.async_start_new_kernel(**kwargs)
          await self.async_start_new_kernel_client()
      try:
          yield
      except RuntimeError as e:
          await run_hook(self.on_notebook_error, notebook=self.nb)
          raise e
      finally:
          if cleanup_kc:
              await self._async_cleanup_kernel()
          await run_hook(self.on_notebook_complete, notebook=self.nb)

  async def process_message(
      self,
      msg: t.Dict,
      cell: NotebookNode,
      cell_index: int) -> t.Optional[t.List]:
    """
    Processes a kernel message, updates cell state, and returns the
    resulting output object that was appended to cell.outputs.

    The input argument *cell* is modified in-place.

    Parameters
    ----------
    msg : dict
      The kernel message being processed.
    cell : nbformat.NotebookNode
      The cell which is currently being processed.
    cell_index : int
      The position of the cell within the notebook object.

    Returns
    -------
    output : dict
      The execution output payload (or None for no output).

    Raises
    ------
    CellExecutionComplete
      Once a message arrives which indicates computation completeness.

    """
    msg_type = msg['msg_type']
    self.log.debug("msg_type: %s", msg_type)
    content = msg['content']
    self.log.debug("content: %s", content)

    display_id = content.get('transient', {}).get('display_id', None)
    if display_id and msg_type in {'execute_result', 'display_data', 'update_display_data'}:
      self._update_display_id(display_id, msg)

    # set the prompt number for the input and the output
    if 'execution_count' in content:
      cell['execution_count'] = content['execution_count']

    if self.record_timing:
      if msg_type == 'status':
        if content['execution_state'] == 'idle':
          cell['metadata']['execution']['iopub.status.idle'] = timestamp()
        elif content['execution_state'] == 'busy':
          cell['metadata']['execution']['iopub.status.busy'] = timestamp()
      elif msg_type == 'execute_input':
        cell['metadata']['execution']['iopub.execute_input'] = timestamp()

    if msg_type == 'status':
      if content['execution_state'] == 'idle':
        raise CellExecutionComplete()
    elif msg_type == 'clear_output':
      self.clear_output(cell.outputs, msg, cell_index)
    elif msg_type.startswith('comm'):
      await self.handle_comm_msg(cell.outputs, msg, cell_index)
    # Check for remaining messages we don't process
    elif msg_type not in ['execute_input', 'update_display_data']:
      # Assign output as our processed "result"
      return self.output(cell.outputs, msg, display_id, cell_index)
    return None
