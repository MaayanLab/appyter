import itertools

from appyter.ext.pathlib.chroot import ChrootPurePosixPath

def parent_url(url):
  parent, *filename = url.rsplit('/', maxsplit=1)
  return parent if filename else ''

def url_filename(url):
  parent, *filename = url.rsplit('/', maxsplit=1)
  return filename[0] if filename else parent

def join_slash(*parts):
  if not parts: return ''
  part0, *parts = parts
  return '/'.join(itertools.chain((part0.rstrip('/'),), (part.lstrip('/') for part in parts)))

def join_url(root, *parts):
  return join_slash(root, str(ChrootPurePosixPath('/').join(*parts)))
