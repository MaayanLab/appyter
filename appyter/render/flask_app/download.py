import os
import shutil
import tempfile
import traceback
import urllib.request, urllib.error
from flask import request, copy_current_request_context, current_app, session
from flask_socketio import emit

from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.util import secure_filename, secure_url, sha1sum_file, generate_uuid

# remove user agent from urllib.request requests
_opener = urllib.request.build_opener()
_opener.addheaders = [('Accept', '*/*')]
urllib.request.install_opener(_opener)


# organize file by content hash
def organize_file_content(path):
  content_hash = sha1sum_file(path)
  content_path = os.path.join(current_app.config['DATA_DIR'], 'input', content_hash)
  if not os.path.exists(content_path):
    os.makedirs(os.path.dirname(content_path), exist_ok=True)
    shutil.move(path, content_path)
    os.chmod(content_path, 400)
  else:
    os.remove(path)
  return content_hash


# download from remote
@socketio.on('download_start')
def download(data):
  session_dir = os.path.join(current_app.config['DATA_DIR'], 'tmp', secure_filename(request.sid))
  os.makedirs(session_dir, exist_ok=True)
  name = data.get('name')
  # TODO: hash based on url?
  # TODO: s3 bypass
  url = secure_url(data.get('url'))
  filename = secure_filename(data.get('file'))
  # TODO: worry about files that are too big/long
  @copy_current_request_context
  def download_with_progress_and_hash(name, url, path, filename, emit):
    emit('download_start', dict(name=name, filename=filename))
    try:
      _, response = urllib.request.urlretrieve(
        url,
        filename=path,
        reporthook=lambda chunk, chunk_size, total_size: emit(
          'download_progress', dict(
            name=name,
            chunk=chunk,
            chunk_size=chunk_size,
            total_size=total_size,
          )
        ),
      )
      # NOTE: this may become an issue if ever someone wants actual html
      assert response.get_content_type() != 'text/html', 'Expected data, got html'
    except Exception as e:
      print('download error')
      traceback.print_exc()
      emit('download_error', dict(name=name, filename=filename, url=url, error=str(e)))
    else:
      emit('download_complete', dict(
        name=name, filename=filename,
        full_filename='/'.join((organize_file_content(path), filename)),
      ))
  #
  emit('download_queued', dict(name=name, filename=filename))
  socketio.start_background_task(
    download_with_progress_and_hash,
    name=name,
    url=url,
    path=os.path.join(session_dir, generate_uuid()),
    filename=filename,
    emit=emit,
  )


# upload from client
@socketio.on("siofu_start")
def siofu_start(data):
  try:
    session_dir = os.path.join(current_app.config['DATA_DIR'], 'tmp', secure_filename(request.sid))
    path = os.path.join(session_dir, generate_uuid())
    filename = secure_filename(data.get('name'))
    os.makedirs(session_dir, exist_ok=True)
    session[request.sid] = dict(session.get(request.sid, {}), **{
      'file_%d' % (data.get('id')): dict(data,
        path=path,
        name=filename,
        bytesLoaded=0,
        fh=open(path, 'wb'),
      ),
    })
    emit('siofu_ready', {
      'id': data.get('id'),
      'name': None,
    })
  except Exception as e:
    traceback.print_exc()
    emit('siofu_error', str(e))

@socketio.on("siofu_progress")
def siofu_progress(evt):
  session[request.sid]['file_%d' % (evt['id'])]['fh'].write(evt['content'])
  print('progress', evt)
  emit("siofu_chunk", dict(
    id=evt['id'],
  ))

@socketio.on("siofu_done")
def siofu_done(evt):
  session[request.sid]['file_%d' % (evt['id'])]['fh'].close()
  path = session[request.sid]['file_%d' % (evt['id'])]['path']
  filename = session[request.sid]['file_%d' % (evt['id'])]['name']
  del session[request.sid]['file_%d' % (evt['id'])]
  emit('siofu_complete', dict(
    id=evt['id'],
    detail=dict(
      full_filename='/'.join((organize_file_content(path), filename)),
    )
  ))


# upload from client with POST
def upload_from_request(req, fnames):
  data = dict()
  for fname in fnames:
    fh = req.files.get(fname)
    if fh:
      filename = secure_filename(fh.filename)
      with tempfile.TemporaryDirectory(dir=os.path.join(current_app.config['DATA_DIR'], 'tmp')) as tmpdir:
        path = os.path.join(tmpdir, filename)
        fh.save(path)
        data[fname] = '/'.join((organize_file_content(path), filename))
  return data
