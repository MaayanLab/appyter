# Custom execute processor derived directly from ExecutePreprocessor source code
#  we split up the preprocess method into setup, preprocess, and destroy with our
#  new preprocess yielding results as they are available.
import os
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

class YieldingExecutePreprocessor(ExecutePreprocessor):
  def __init__(self, *args, env=os.environ, **kwargs):
    super().__init__(*args, **kwargs)
    self.env = env

  def setup_preprocess(self, nb, resources):
    path = resources.get('metadata', {}).get('path', '')
    if path == '':
      path = None
    else:
      os.makedirs(path, exist_ok=True)

    # clear display_id map
    self._display_id_map = {}

    # from jupyter_client.manager import start_new_kernel

    def start_new_kernel(startup_timeout=None, kernel_name='python', **kwargs):
      km = self.kernel_manager_class(kernel_name=kernel_name)
      km.start_kernel(env=self.env, **kwargs)
      kc = km.client()
      kc.start_channels()
      try:
        kc.wait_for_ready(timeout=startup_timeout)
      except RuntimeError:
        kc.stop_channels()
        km.shutdown_kernel()
        raise

      return km, kc

    kernel_name = nb.metadata.get('kernelspec', {}).get('name', 'python')
    if self.kernel_name:
      kernel_name = self.kernel_name
    self.log.info("Executing notebook with kernel: %s" % kernel_name)
    self.km, self.kc = start_new_kernel(
      startup_timeout=self.startup_timeout,
      kernel_name=kernel_name,
      extra_arguments=self.extra_arguments,
      cwd=path)
    self.kc.allow_stdin = False
    self.nb = nb

  def preprocess(self, nb, resources):
    self.setup_preprocess(nb, resources)
    try:
      for index, cell in enumerate(nb.cells):
        nb.cells[index], resources = self.preprocess_cell(cell, resources, index)
        yield (nb.cells[index], resources)
    except Exception as e:
      raise e
    finally:
      self.destroy_preprocess()

  def destroy_preprocess(self):
    self.kc.stop_channels()
    self.km.shutdown_kernel(now=self.shutdown_kernel == 'immediate')
    delattr(self, 'nb')
