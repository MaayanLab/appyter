import os
import shutil
import tempfile
import traceback
import urllib.request, urllib.error
from flask import request, copy_current_request_context, current_app, session
from flask_socketio import emit

from appyter.ext.fs import Filesystem
from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.util import secure_filename, secure_url, sha1sum_io, generate_uuid

# remove user agent from urllib.request requests
_opener = urllib.request.build_opener()
_opener.addheaders = [('Accept', '*/*')]
urllib.request.install_opener(_opener)


# organize file by content hash
def organize_file_content(tmp_fs, path):
  content_hash = sha1sum_io(tmp_fs.open(path, 'rb'))
  data_fs = Filesystem(Filesystem.join(current_app.config['DATA_DIR'], 'input'))
  if not data_fs.exists(content_hash):
    Filesystem.mv(src_fs=tmp_fs, src_path=path, dst_fs=data_fs, dst_path=content_hash)
    data_fs.chmod_ro(content_hash)
  else:
    tmp_fs.rm(path)
  return content_hash


# download from remote
@socketio.on('download_start')
def download(data):
  tmp_fs = Filesystem('tmpfs://')
  session_dir = secure_filename(request.sid)
  tmp_fs.makedirs(session_dir, exist_ok=True)
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
      req = urllib.request.urlopen(url)
      headers = req.info()
      # NOTE: this may become an issue if ever someone wants actual html
      assert headers.get('Content-Type') != 'text/html', 'Expected data, got html'
      chunk = 0
      chunk_size = 1024*8
      total_size = headers.get('Content-Length', -1)
      reporthook = lambda chunk, name=name, chunk_size=chunk_size, total_size=total_size: emit(
        'download_progress', dict(name=name, chunk=chunk, chunk_size=chunk_size, total_size=total_size)
      )
      with tmp_fs.open(path, 'wb') as fw:
        reporthook(chunk)
        while buf := req.read(chunk_size):
          fw.write(buf)
          chunk += 1
          reporthook(chunk)
    except Exception as e:
      print('download error')
      traceback.print_exc()
      emit('download_error', dict(name=name, filename=filename, url=url, error=str(e)))
    else:
      emit('download_complete', dict(
        name=name, filename=filename,
        full_filename='/'.join((organize_file_content(tmp_fs, path), filename)),
      ))
  #
  emit('download_queued', dict(name=name, filename=filename))
  socketio.start_background_task(
    download_with_progress_and_hash,
    name=name,
    url=url,
    path=Filesystem.join(session_dir, generate_uuid()),
    filename=filename,
    emit=emit,
  )


# upload from client
@socketio.on("siofu_start")
def siofu_start(data):
  try:
    tmp_fs = Filesystem('tmpfs://')
    session_dir = secure_filename(request.sid)
    path = Filesystem.join(session_dir, generate_uuid())
    filename = secure_filename(data.get('name'))
    tmp_fs.makedirs(session_dir, exist_ok=True)
    session[request.sid] = dict(session.get(request.sid, {}), **{
      'file_%d' % (data.get('id')): dict(data,
        path=path,
        name=filename,
        bytesLoaded=0,
        fh=tmp_fs.open(path, 'wb'),
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
  tmp_fs = Filesystem('tmpfs://')
  session[request.sid]['file_%d' % (evt['id'])]['fh'].close()
  path = session[request.sid]['file_%d' % (evt['id'])]['path']
  filename = session[request.sid]['file_%d' % (evt['id'])]['name']
  del session[request.sid]['file_%d' % (evt['id'])]
  emit('siofu_complete', dict(
    id=evt['id'],
    detail=dict(
      full_filename='/'.join((organize_file_content(tmp_fs, path), filename)),
    )
  ))


# upload from client with POST
def upload_from_request(req, fnames):
  data = dict()
  for fname in fnames:
    fh = req.files.get(fname)
    if fh:
      filename = secure_filename(fh.filename)
      path = generate_uuid()
      tmp_fs = Filesystem('tmpfs://')
      fh.save(tmp_fs.open(path, 'w'))
      data[fname] = '/'.join((organize_file_content(tmp_fs, path), filename))
  return data
