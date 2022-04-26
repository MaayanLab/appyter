'''
Constants that can be cached in thread-local storage
'''

from appyter.ext.functools import memcached
from appyter.ext.flask import decorator_in_production

@decorator_in_production(memcached)
def get_env():
  try:
    from flask import current_app
    return current_app.config
  except RuntimeError:
    from appyter.context import get_env
    return get_env()

@decorator_in_production(memcached)
def get_cwd_fs():
  ''' Return fsspec compatible chroot to the current directory
  '''
  from appyter.ext.fsspec.core import url_to_chroot_fs
  return url_to_chroot_fs(get_env()['CWD'])

@decorator_in_production(memcached)
def get_static_fs():
  ''' Return fsspec compatible chroot to the static directory
  '''
  from appyter.ext.fsspec.core import url_to_chroot_fs
  return url_to_chroot_fs(get_env()['STATIC_DIR'])

@decorator_in_production(memcached)
def get_input_fs():
  ''' Return fsspec compatible chroot to the static directory
  '''
  from appyter.ext.fsspec.core import url_to_chroot_fs
  return url_to_chroot_fs('storage://input/')

@decorator_in_production(memcached)
def get_output_fs():
  ''' Return fsspec compatible chroot to the static directory
  '''
  from appyter.ext.fsspec.core import url_to_chroot_fs
  return url_to_chroot_fs('storage://output/')

@decorator_in_production(memcached)
def _get_ipynb_io():
  ''' Return byte stream for original ipynb
  '''
  import io, shutil
  ipynb_io = io.BytesIO()
  with get_cwd_fs().open(get_env()['IPYNB'], 'rb') as fr:
    shutil.copyfileobj(fr, ipynb_io)
  return ipynb_io

def get_ipynb_io():
  ''' Reuse the BytesIO stream
  '''
  ipynb_io = _get_ipynb_io()
  ipynb_io.seek(0)
  return ipynb_io

@decorator_in_production(memcached)
def get_nbtemplate():
  ''' Parse the ipynb
  '''
  from appyter.parse.nb import nb_from_ipynb_io
  return nb_from_ipynb_io(get_ipynb_io())

@decorator_in_production(memcached)
def get_j2_env():
  ''' Get an initialized bare jinja2 environment (no context)
  '''
  from appyter.context import get_jinja2_env
  return get_jinja2_env(config=get_env())

@decorator_in_production(memcached)
def get_form():
  ''' Render a form for the nbtemplate
  '''
  from appyter.render.form import render_form_from_nbtemplate
  return render_form_from_nbtemplate(get_j2_env(), get_nbtemplate())

@decorator_in_production(memcached)
def get_nbtemplate_json():
  ''' Render the nbtemplate as nbtemplate_json
  '''
  from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
  return render_nbtemplate_json_from_nbtemplate(get_j2_env(), get_nbtemplate())

@decorator_in_production(memcached)
def get_fields():
  ''' Parse the nbtemplate fields
  '''
  from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
  return parse_fields_from_nbtemplate(get_j2_env(), get_nbtemplate(), deep=False)

@decorator_in_production(memcached)
def get_deep_fields():
  ''' Parse the nbtemplate fields
  '''
  from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
  return parse_fields_from_nbtemplate(get_j2_env(), get_nbtemplate(), deep=True)

@decorator_in_production(memcached)
def get_ipynb_hash():
  ''' A hash for the ipynb
  '''
  from appyter.ext.hashlib import sha1sum_io
  return sha1sum_io(get_ipynb_io())

@decorator_in_production(memcached)
def get_html_exporer():
  ''' nbconvert html export
  '''
  from nbconvert import HTMLExporter
  html_exporter = HTMLExporter()
  html_exporter.template_name = 'classic'
  return html_exporter

@decorator_in_production(memcached)
def get_base_files():
  ''' Include all (non-hidden) files in cwd (include requirements.txt, utils, etc..)
  '''
  fs = get_cwd_fs()
  ipynb = get_env()['IPYNB']
  base_files = {}
  for f in fs.glob('*'):
    if f.startswith('.'): continue
    if f == ipynb: continue
    if not fs.isfile(f): continue
    base_files[f] = fs.open(f, 'rb').read()
  return base_files
