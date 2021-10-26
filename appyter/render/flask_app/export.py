''' Endpoints for exporting results
'''
import os
import io
import zipfile
from flask import request, current_app, send_file, abort
from nbconvert import HTMLExporter

from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.render.flask_app.core import core
from appyter.ext.flask import route_join_with_or_without_slash
from appyter.parse.nb import nb_from_ipynb_io

_html_exporter = None
def get_html_exporer():
  ''' nbconvert html export
  '''
  global _html_exporter
  if _html_exporter is None:
    _html_exporter = HTMLExporter()
    _html_exporter.template_name = 'classic'
  return _html_exporter

_base_files = None
def get_base_files():
  ''' Include all (non-hidden) files in cwd (include requirements.txt, utils, etc..)
  '''
  global _base_files
  if _base_files is None:
    _base_files = {}
    fs = url_to_chroot_fs(current_app.config['CWD'])
    for f in fs.glob('*'):
      if f.startswith('.'): continue
      if f == current_app.config['IPYNB']: continue
      _base_files[f] = fs.open(f, 'rb').read()
  return _base_files

@route_join_with_or_without_slash(core, 'export', '<path:path>', methods=['GET'])
def export(path):
  if path.endswith('/'):
    format = request.args.get('format', 'html')
    data_fs = url_to_chroot_fs('storage:///output/')
    nbpath = path + current_app.config['IPYNB']
    if data_fs.exists(nbpath):
      nb = nb_from_ipynb_io(data_fs.open(nbpath, 'rb'))
      if format == 'html':
        exporter = get_html_exporer()
        body, _rcs = exporter.from_notebook_node(nb)
        return send_file(io.BytesIO(body.encode()), mimetype='text/html', as_attachment=True, attachment_filename='output.html')
      elif format == 'zip':
        metadata = nb.get('metadata', {}).get('appyter', {})
        files = metadata.get('nbexecute', {}).get('files', metadata.get('nbconstruct', {}).get('files', {}))
        with url_to_chroot_fs('tmpfs://') as tmp_fs:
          with tmp_fs.open('output.zip', 'wb') as fw:
            with zipfile.ZipFile(fw, 'a', zipfile.ZIP_DEFLATED, False) as zf:
              for f, b in get_base_files().items():
                zf.writestr(f, b)
              for f, p in ([(os.path.basename(nbpath), nbpath)] + [(f, path+f) for f in files]):
                if data_fs.exists(p):
                  with data_fs.open(p, 'rb') as fr:
                    zf.writestr(f, fr.read())
          return send_file(tmp_fs.open('output.zip', 'rb'), mimetype='application/zip', as_attachment=True, attachment_filename='output.zip')
  abort(404)
