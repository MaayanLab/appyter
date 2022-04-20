import re
from appyter.ext.urllib import url_filename
from appyter.render.flask_app.constants import get_input_fs
from appyter.ext.fsspec.core import url_to_fs_ex
from appyter.ext.contextlib import ensure_context
from appyter.render.flask_app.upload import organize_file_content
from appyter.context import get_env

def ensure_drs(url):
  ''' Ensures a url is accessible via DRS
  '''
  if url.startswith('storage://input/'):
    return url_filename(url)
  #
  fs, fo = url_to_fs_ex(url)
  try:
    # Some providers, namely SBFS, provide DRS endpoints already
    return fs.get_drs(fo)
  except AttributeError:
    pass
  #
  with ensure_context(fs) as fs:
    storage_id = organize_file_content(get_input_fs(), fs, fo)
  #
  env = get_env()
  drs_id = re.sub(r"^storage://input/", re.sub(r'^https?://', 'drs://', env['PUBLIC_URL'] + '/'), storage_id)
  return drs_id
