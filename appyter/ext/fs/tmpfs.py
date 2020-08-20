import tempfile
import urllib.parse
from appyter.ext.fs.file import Filesystem as FSFilesystem

class Filesystem(FSFilesystem):
  def __init__(self, uri):
    self._tmpdir = tempfile.mkdtemp(dir=uri.path) if uri.path else tempfile.mkdtemp()
    super().__init__(urllib.parse.urlparse('file://' + self._tmpdir))
  #
  def __del__(self):
    self.rm(self._uri.path, recursive=True)
