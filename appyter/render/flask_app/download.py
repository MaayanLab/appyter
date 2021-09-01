import aiohttp
import traceback
import logging
logger = logging.getLogger(__name__)

from appyter.ext.fs import Filesystem
from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.util import secure_filepath, secure_url, sha1sum_io, generate_uuid

# organize file by content hash
def organize_file_content(data_fs, tmp_fs, tmp_path):
  with tmp_fs.open(tmp_path, 'rb') as fr:
    content_hash = sha1sum_io(fr)
  data_path = Filesystem.join('input', content_hash)
  if not data_fs.exists(data_path):
    Filesystem.mv(src_fs=tmp_fs, src_path=tmp_path, dst_fs=data_fs, dst_path=data_path)
    data_fs.chmod_ro(data_path)
  return content_hash

# download from remote
async def download_with_progress_and_hash(sid, data_fs, name, url, path, filename):
  # TODO: worry about files that are too big/long
  with Filesystem('tmpfs://') as tmp_fs:
    await socketio.emit('download_start', dict(name=name, filename=filename), room=sid)
    try:
      async with aiohttp.ClientSession() as client:
        async with client.get(url) as resp:
          # NOTE: this may become an issue if ever someone wants actual html
          assert resp.content_type != 'text/html', 'Expected data, got html'
          resp.headers.get('Content-Length', -1)
          chunk = 0
          chunk_size = 1024*8
          total_size = resp.headers.get('Content-Length', -1)
          async def reporthook(chunk):
            await socketio.emit(
              'download_progress',
              dict(name=name, chunk=chunk, chunk_size=chunk_size, total_size=total_size),
              room=sid,
            )
          with tmp_fs.open(path, 'wb') as fw:
            await reporthook(chunk)
            while True:
              buf = await resp.content.read(chunk_size)
              if not buf: break
              fw.write(buf)
              chunk += 1
              await reporthook(chunk)
    except Exception as e:
      logger.error(f"download error: {traceback.format_exc()}")
      await socketio.emit(
        'download_error',
        dict(name=name, filename=filename, url=url, error=str(e)),
        room=sid,
      )
    else:
      await socketio.emit(
        'download_complete',
        dict(
          name=name, filename=filename,
          full_filename='/'.join((organize_file_content(data_fs, tmp_fs, path), filename)),
        ),
        room=sid,
      )

@socketio.on('download_start')
async def download(sid, data):
  async with socketio.session(sid) as sess:
    config = sess['config']
  #
  data_fs = Filesystem(config['DATA_DIR'])
  name = data.get('name')
  # TODO: hash based on url?
  # TODO: s3 bypass
  url = secure_url(data.get('url'))
  filename = secure_filepath(data.get('file'))
  await socketio.emit('download_queued', dict(name=name, filename=filename), room=sid)
  await download_with_progress_and_hash(
    sid=sid,
    data_fs=data_fs,
    name=name,
    url=url,
    path=generate_uuid(),
    filename=filename,
  )


# upload from client
@socketio.on("siofu_start")
async def siofu_start(sid, data):
  try:
    path = generate_uuid()
    filename = secure_filepath(data.get('name'))
    tmp_fs = Filesystem('tmpfs://')
    async with socketio.session(sid) as sess:
      sess['file_%d' % (data.get('id'))] = dict(
        data,
        path=path,
        name=filename,
        bytesLoaded=0,
        tmp_fs=tmp_fs,
        fh=tmp_fs.open(path, 'wb'),
      )
    await socketio.emit(
      'siofu_ready',
      {
        'id': data.get('id'),
        'name': None,
      },
      room=sid,
    )
  except Exception as e:
    logger.error(traceback.format_exc())
    await socketio.emit('siofu_error', str(e), room=sid)

@socketio.on("siofu_progress")
async def siofu_progress(sid, evt):
  async with socketio.session(sid) as sess:
    sess['file_%d' % (evt['id'])]['fh'].write(evt['content'])
  logger.debug(f"progress: {evt}")
  await socketio.emit("siofu_chunk", dict(
    id=evt['id'],
  ), room=sid)

@socketio.on("siofu_done")
async def siofu_done(sid, evt):
  async with socketio.session(sid) as sess:
    sess['file_%d' % (evt['id'])]['fh'].close()
    config = sess['config']
    data_fs = Filesystem(config['DATA_DIR'])
    tmp_fs = sess['file_%d' % (evt['id'])]['tmp_fs']
    path = sess['file_%d' % (evt['id'])]['path']
    filename = sess['file_%d' % (evt['id'])]['name']
    content_hash = organize_file_content(data_fs, tmp_fs, path)
    tmp_fs.close()
    del sess['file_%d' % (evt['id'])]
  #
  await socketio.emit('siofu_complete', dict(
    id=evt['id'],
    detail=dict(
      full_filename='/'.join((content_hash, filename)),
    )
  ), room=sid)

# upload from client with POST
def upload_from_request(req, fnames):
  from flask import current_app
  data_fs = Filesystem(current_app.config['DATA_DIR'])
  data = dict()
  for fname in fnames:
    fh = req.files.get(fname)
    if fh:
      filename = secure_filepath(fh.filename)
      path = generate_uuid()
      with Filesystem('tmpfs://') as tmp_fs:
        with tmp_fs.open(path, 'wb') as fw:
          fh.save(fw)
        data[fname] = '/'.join((organize_file_content(data_fs, tmp_fs, path), filename))
  return data
