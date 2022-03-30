''' Endpoints for exporting results
'''
import io
import shutil
import zipfile
from flask import request, current_app, send_file, abort

from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.render.flask_app.constants import get_base_files, get_html_exporer
from appyter.render.flask_app.core import core, prepare_storage
from appyter.ext.flask import route_join_with_or_without_slash
from appyter.parse.nb import nb_from_ipynb_io

@route_join_with_or_without_slash(core, 'export', '<path:path>', methods=['GET'])
def export(path):
  if path.endswith('/'):
    data = { '_id': path }
    if 'catalog-integration' in current_app.config['EXTRAS']:
      from appyter.extras.catalog_integration.request import prepare_data as prepare_data_catalog
      data.update(prepare_data_catalog(request))
    format = request.args.get('format', 'html')
    with prepare_storage(data) as data_fs:
      nbpath = current_app.config['IPYNB']
      if data_fs.exists(nbpath):
        with data_fs.open(nbpath, 'rb') as fr:
          nb = nb_from_ipynb_io(fr)
        if format == 'html':
          exporter = get_html_exporer()
          body, _rcs = exporter.from_notebook_node(nb)
          return send_file(io.BytesIO(body.encode()), mimetype='text/html', as_attachment=True, attachment_filename='output.html')
        elif format == 'zip':
          metadata = nb.get('metadata', {}).get('appyter', {})
          files = metadata.get('nbexecute', {}).get('files', metadata.get('nbconstruct', {}).get('files', {}))
          with url_to_chroot_fs('memory://') as tmp_fs:
            with tmp_fs.open('output.zip', 'wb') as fw:
              with zipfile.ZipFile(fw, 'a', zipfile.ZIP_DEFLATED, False) as zf:
                for f, b in get_base_files().items():
                  zf.writestr(f, b)
                for f in (nbpath, *files):
                  if data_fs.exists(f):
                    with data_fs.open(f, 'rb') as fr:
                      with zf.open(f, 'w') as zfw:
                        shutil.copyfileobj(fr, zfw)
            return send_file(tmp_fs.open('output.zip', 'rb'), mimetype='application/zip', as_attachment=True, attachment_filename='output.zip')
  abort(404)
