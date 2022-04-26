import traceback
import logging
import shutil
from fsspec.core import url_to_fs
from flask import request, jsonify, abort
from appyter.ext.asyncio.helpers import ensure_async, ensure_sync
from appyter.ext.contextlib import ContextManagerAsHandle

from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.urllib import URI
from appyter.render.flask_app.constants import get_input_fs
logger = logging.getLogger(__name__)

from appyter.render.flask_app.core import core
from appyter.render.flask_app.socketio import socketio
from appyter.render.flask_app.prepare import prepare_storage, prepare_request
from appyter.ext.flask import secure_filepath, route_join_with_or_without_slash
from appyter.ext.hashlib import sha1sum_io
from appyter.ext.uuid import generate_uuid

# organize file by content hash
def organize_file_content(data_fs, tmp_fs, tmp_path, filename=None):
  with tmp_fs.open(tmp_path, 'rb') as fr:
    content_hash = sha1sum_io(fr)
  if not data_fs.exists(content_hash):
    with tmp_fs.open(tmp_path, 'rb') as fr:
      with data_fs.open(content_hash, 'wb') as fw:
        shutil.copyfileobj(fr, fw)
  return f"storage://input/{content_hash}{('#' + filename) if filename else ''}"

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
    tmp_fs_ctx = ContextManagerAsHandle(url_to_chroot_fs('memory:///'))
    tmp_fs = tmp_fs_ctx.open()
    async with socketio.session(sid) as sess:
      sess['file_%d' % (data.get('id'))] = dict(
        data,
        path=path,
        name=filename,
        bytesLoaded=0,
        tmp_fs_ctx=tmp_fs_ctx,
        tmp_fs=tmp_fs,
        fh=tmp_fs.open(path, 'wb'),
      )
    await socketio.emit(
      'siofu_ready',
      {
        'id': data.get('id'),
        'name': None,
      },
      to=sid,
    )
  except Exception as e:
    logger.error(traceback.format_exc())
    await socketio.emit('siofu_error', str(e), to=sid)

@socketio.on("siofu_progress")
async def siofu_progress(sid, evt):
  async with socketio.session(sid) as sess:
    sess['file_%d' % (evt['id'])]['fh'].write(evt['content'])
  logger.debug(f"progress: {evt}")
  await socketio.emit("siofu_chunk", dict(
    id=evt['id'],
  ), to=sid)

@socketio.on("siofu_done")
async def siofu_done(sid, evt):
  async with socketio.session(sid) as sess:
    fid = 'file_%d' % (evt['id'])
    file = sess[fid]
    file['fh'].close()
    input_fs = get_input_fs()
    tmp_fs_ctx = file['tmp_fs_ctx']
    file_uri = await ensure_async(organize_file_content)(input_fs, file['tmp_fs'], file['path'], file['name'])
    tmp_fs_ctx.close()
    #
    if 'catalog-integration' in sess['config']['EXTRAS']:
      # if you upload a file in a request, it should get registered
      try:
        from appyter.extras.catalog_integration.uploads import FileInfo, add_file
        file_uri_parsed = URI(file_uri)
        await add_file(
          FileInfo(
            file=str(file_uri_parsed.with_fragment(None)),
            filename=file_uri_parsed.fragment,
            metadata=dict(
              size=file['size'],
            ),
          ),
          auth=file.get('meta', {}).get('auth'),
          config=sess['config'],
        )
      except:
        logger.warning(traceback.format_exc())
    #
    del sess[fid]
  #
  await socketio.emit('siofu_complete', dict(
    id=evt['id'],
    detail=dict(full_filename=file_uri)
  ), to=sid)

# upload from client with POST
def upload_from_request(req, fname):
  fh = req.files.get(fname)
  if not fh: return None
  filename = secure_filepath(fh.filename)
  if not filename: return None
  data = prepare_request(req)
  with url_to_chroot_fs(str(URI(prepare_storage(data)).join('input'))) as input_fs:
    path = generate_uuid()
    with url_to_chroot_fs('memory:///') as tmp_fs:
      with tmp_fs.open(path, 'wb') as fw:
        fh.save(fw)
      file_uri = organize_file_content(input_fs, tmp_fs, path, filename)
  #
  if 'catalog-integration' in data['_config']['EXTRAS']:
    # if you upload a file in a request, it should get registered
    try:
      from appyter.extras.catalog_integration.uploads import FileInfo, add_file
      file_uri_parsed = URI(file_uri)
      ensure_sync(add_file(
        FileInfo(file=str(file_uri_parsed.with_fragment(None)), filename=file_uri_parsed.fragment),
        auth=data.get('_auth'),
        config=data.get('_config'),
      ))
    except:
      logger.warning(traceback.format_exc())
  #
  return file_uri
