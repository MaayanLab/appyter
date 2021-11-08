import shutil
import logging
logger = logging.getLogger(__name__)

from fsspec import filesystem, AbstractFileSystem
from fsspec.core import url_to_fs
from appyter.ext.fsspec.parse import parse_file_uri_qs
from appyter.ext.urllib import join_slash

class OverlayFileSystem(AbstractFileSystem):
  ''' OverlayFS implemented with fsspec
  '''
  root_marker = ''
  protocol = 'overlayfs'

  def __init__(self, lower=None, upper=None, **kwargs):
    '''
    Parameters
    ----------
    lower: str | fs | (protocol, options) initial
    upper: str | fs | (protocol, options) writes go here
    '''
    super().__init__(**kwargs)
    if (lower is None) or (upper is None):
      raise ValueError(
          "Please provide lower & upper"
      )

    if type(lower) == str:
      self.lower = url_to_fs(lower)
    elif isinstance(lower, AbstractFileSystem):
      self.lower = lower
    else:
      protocol, opts = lower
      self.lower = filesystem(protocol, **opts)

    if type(upper) == str:
      self.upper = url_to_fs(upper)
    elif isinstance(upper, AbstractFileSystem):
      self.upper = upper
    else:
      protocol, opts = upper
      self.upper = filesystem(protocol, **opts)

  def __enter__(self):
    if getattr(self.lower, '__enter__', None) is not None:
      self.lower.__enter__()
    if getattr(self.upper, '__enter__', None) is not None:
      self.upper.__enter__()
    return self
  
  def __exit__(self, type, value, traceback):
    if getattr(self.upper, '__exit__', None) is not None:
      self.upper.__exit__(type, value, traceback)
    if getattr(self.lower, '__exit__', None) is not None:
      self.lower.__exit__(type, value, traceback)

  def mkdir(self, path, **kwargs):
    return self.upper.mkdir(path, **kwargs)

  def rm(self, path, recursive=False, maxdepth=None):
    return self.upper.rm(path, recursive=recursive, maxdepth=maxdepth)

  def copy(self, path1, path2, recursive=False, on_error=None, maxdepth=None, **kwargs):
    if self.upper.exists(path1) or not self.lower.exists(path1):
      return self.upper.copy(path1, path2, recursive=recursive, on_error=on_error, maxdepth=maxdepth, **kwargs)
    else:
      if self.lower.isdir(path1) and recursive:
        for f1 in self.lower.walk(path1, maxdepth=maxdepth):
          f_rel = f1.replace(path1, '')
          f2_rel = join_slash(path2, f_rel)
          with self.lower.open(f1, 'rb') as fr:
            with self.upper.open(f2_rel, 'wb') as fw:
              shutil.copyfileobj(fr, fw)
      else:
        with self.lower.open(path1, 'rb') as fr:
          with self.upper.open(path2, 'wb') as fw:
            shutil.copyfileobj(fr, fw)

  def mv(self, path1, path2, recursive=False, maxdepth=None, **kwargs):
    if self.upper.exists(path1):
      return self.upper.mv(path1, path2, recursive=recursive, maxdepth=maxdepth, **kwargs)
    else:
      raise PermissionError(path1)

  def exists(self, path, **kwargs):
    return self.upper.exists(path, **kwargs) or self.lower.exists(path, **kwargs)

  def info(self, path, **kwargs):
    if self.upper.exists(path) or not self.lower.exists(path):
      return self.upper.info(path, **kwargs)
    else:
      return self.lower.info(path, **kwargs)

  def ls(self, path, detail=False, **kwargs):
    results = {}
    for info in self.lower.ls(path, detail=detail, **kwargs):
      if detail:
        results[info['name']] = info
      else:
        results[info] = info

    for info in self.upper.ls(path, detail=detail, **kwargs):
      if detail:
        results[info['name']] = info
      else:
        results[info] = info
    
    return list(results.values())

  def _open(self, path, mode="rb", block_size=None, autocommit=True, cache_options=None, **kwargs):
    if 'w' in mode:
      pass
    elif 'a' in mode or '+' in mode:
      if not self.upper.exists(path):
        with self.lower.open(path, 'rb') as fr:
          with self.upper.open(path, 'wb') as fw:
            shutil.copyfileobj(fr, fw)
    elif self.upper.exists(path):
      pass
    elif self.lower.exists(path):
      # completely readonly and only exists in lower
      return self.lower._open(
        path,
        mode=mode,
        block_size=block_size,
        autocommit=autocommit,
        cache_options=cache_options,
        **kwargs
      )
    #
    return self.upper._open(
      path,
      mode=mode,
      block_size=block_size,
      autocommit=autocommit,
      cache_options=cache_options,
      **kwargs
    )
