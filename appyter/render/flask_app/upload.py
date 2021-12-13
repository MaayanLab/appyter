import aiohttp
import traceback
import logging
import shutil
from fsspec.core import url_to_fs
from flask import request, jsonify, abort

from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.render.flask_app.constants import get_input_fs
logger = logging.getLogger(__name__)

from appyter.render.flask_app.core import core
from appyter.render.flask_app.socketio import socketio
from appyter.ext.flask import secure_filepath, secure_url, route_join_with_or_without_slash
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

@route_join_with_or_without_slash(core, 'check', '<path:path>', methods=['GET'])
def check(path):
  qs = request.query_string.decode()
  url = path + (('?'+qs) if qs else '')
  fs, fs_path = url_to_fs(url)
  if fs.exists(fs_path):
    return jsonify(fs.info(fs_path))
  else:
    abort(404)

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
