from nbclient import NotebookClient
from nbclient.util import ensure_async
from nbclient.exceptions import CellExecutionComplete

class NotebookClientIOPubHook(NotebookClient):
  ''' A notebook client with the ability to hook into iopub updates
  '''
  def __init__(self, *args, iopub_hook=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.iopub_hook = iopub_hook
    self.kc = None

  async def _async_poll_output_msg(
    self,
    parent_msg_id,
    cell,
    cell_index
  ):
    assert self.kc is not None
    while True:
      msg = await ensure_async(self.kc.iopub_channel.get_msg(timeout=None))
      if msg['parent_header'].get('msg_id') == parent_msg_id:
        try:
          # Will raise CellExecutionComplete when completed
          self.process_message(msg, cell, cell_index)
        except CellExecutionComplete:
          return
        # Process iopub_hook
        if self.iopub_hook is not None:
          await self.iopub_hook(cell, cell_index)
