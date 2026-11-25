import os
import fnmatch
import logging

logger = logging.getLogger(__name__)

class GlobFilter:
  ''' A watchfiles `watch_filter` which only reports changes to files matching
  `include_file_glob` (and not `exclude_file_glob`) by name, inside directories
  which all match `include_dir_glob` (and not `exclude_dir_glob`) by path.

  Directory globs are matched against both the path relative to `root` and
  the absolute path of every directory between `root` and the file, files
  directly in `root` are only subject to the file globs.
  '''
  def __init__(self, root, include_file_glob, include_dir_glob, exclude_file_glob, exclude_dir_glob):
    self.root = os.path.abspath(root)
    self.include_file_glob = include_file_glob
    self.include_dir_glob = include_dir_glob
    self.exclude_file_glob = exclude_file_glob
    self.exclude_dir_glob = exclude_dir_glob

  def should_watch_file(self, name):
    return (
      any(fnmatch.fnmatch(name, g) for g in self.include_file_glob)
      and not any(fnmatch.fnmatch(name, g) for g in self.exclude_file_glob)
    )

  def should_watch_dir(self, rel_path):
    paths = (rel_path, os.path.join(self.root, rel_path))
    match = lambda globs: any(fnmatch.fnmatch(p, g) for p in paths for g in globs)
    return match(self.include_dir_glob) and not match(self.exclude_dir_glob)

  def __call__(self, change, path):
    rel = os.path.relpath(os.path.abspath(path), self.root)
    if rel.startswith('..'): return False
    *dirs, name = rel.split(os.sep)
    for i in range(1, len(dirs)+1):
      if not self.should_watch_dir(os.path.join(*dirs[:i])):
        return False
    return self.should_watch_file(name)
