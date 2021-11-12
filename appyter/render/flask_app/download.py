import aiohttp
import traceback
import logging
import shutil

from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.render.flask_app.constants import get_input_fs
logger = logging.getLogger(__name__)

from appyter.render.flask_app.socketio import socketio
from appyter.ext.flask import secure_filepath, secure_url
from appyter.ext.hashlib import sha1sum_io
from appyter.ext.uuid import generate_uuid

# organize file by content hash
def organize_file_content(data_fs, tmp_fs, tmp_path, filename):
  with tmp_fs.open(tmp_path, 'rb') as fr:
    content_hash = sha1sum_io(fr)
  if not data_fs.exists(content_hash):
    with tmp_fs.open(tmp_path, 'rb') as fr:
      with data_fs.open(content_hash, 'wb') as fw:
        shutil.copyfileobj(fr, fw)
  return f"storage://input/{content_hash}#{filename}"

# download from remote
async def download_with_progress_and_hash(sid, data_fs, name, url, path, filename):
  import asyncio
  # TODO: worry about files that are too big/long
  with url_to_chroot_fs('tmpfs:///') as tmp_fs:
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
          full_filename=await asyncio.get_event_loop().run_in_executor(None, organize_file_content, data_fs, tmp_fs, path, filename),
        ),
        room=sid,
      )

@socketio.on('download_start')
async def download(sid, data):
  input_fs = get_input_fs()
  name = data.get('name')
  # TODO: hash based on url?
  # TODO: s3 bypass
  url = secure_url(data.get('url'))
  filename = secure_filepath(data.get('file'))
  await socketio.emit('download_queued', dict(name=name, filename=filename), room=sid)
  await download_with_progress_and_hash(
    sid=sid,
    data_fs=input_fs,
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
    tmp_fs = url_to_chroot_fs('tmpfs:///')
    async with socketio.session(sid) as sess:
      sess['file_%d' % (data.get('id'))] = dict(
        data,
        path=path,
        name=filename,
        bytesLoaded=0,
        tmp_fs=tmp_fs.__enter__(),
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
  import asyncio
  async with socketio.session(sid) as sess:
    sess['file_%d' % (evt['id'])]['fh'].close()
    input_fs = get_input_fs()
    tmp_fs = sess['file_%d' % (evt['id'])]['tmp_fs']
    path = sess['file_%d' % (evt['id'])]['path']
    filename = sess['file_%d' % (evt['id'])]['name']
    full_filename = await asyncio.get_event_loop().run_in_executor(None, organize_file_content, input_fs, tmp_fs, path, filename)
    tmp_fs.__exit__(None, None, None)
    del sess['file_%d' % (evt['id'])]
  #
  await socketio.emit('siofu_complete', dict(
    id=evt['id'],
    detail=dict(full_filename=full_filename)
  ), room=sid)

# upload from client with POST
def upload_from_request(req, fname):
  input_fs = get_input_fs()
  fh = req.files.get(fname)
  if not fh:
    return None
  filename = secure_filepath(fh.filename)
  path = generate_uuid()
  with url_to_chroot_fs('tmpfs:///') as tmp_fs:
    with tmp_fs.open(path, 'wb') as fw:
      fh.save(fw)
    return organize_file_content(input_fs, tmp_fs, path, filename)
