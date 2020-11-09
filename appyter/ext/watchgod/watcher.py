import fnmatch
import logging
from watchgod.watcher import AllWatcher

logger = logging.getLogger(__name__)

class GlobWatcher(AllWatcher):
  def __init__(self, *args, **kwargs):
    self.include_file_glob = kwargs.pop('include_file_glob')
    self.include_dir_glob = kwargs.pop('include_dir_glob')
    self.exclude_file_glob = kwargs.pop('exclude_file_glob')
    self.exclude_dir_glob = kwargs.pop('exclude_dir_glob')
    super().__init__(*args, **kwargs)

  def should_watch_file(self, entry):
    included = any(
      fnmatch.fnmatch(entry.name, g)
      for g in self.include_file_glob
    )
    excluded = any(
      fnmatch.fnmatch(entry.name, g)
      for g in self.exclude_file_glob
    )
    return included and not excluded

  def should_watch_dir(self, entry):
    included = any(
      fnmatch.fnmatch(entry.path, g)
      for g in self.include_dir_glob
    )
    excluded = any(
      fnmatch.fnmatch(entry.path, g)
      for g in self.exclude_dir_glob
    )
    return included and not excluded
