import re
from flask import Blueprint, abort, jsonify, request
from appyter.ext.fsspec.core import url_to_fs_ex
from appyter.ext.flask import route_join_with_or_without_slash

import logging
logger = logging.getLogger(__name__)

StorageFileField = Blueprint('StorageFileField', __name__)

@route_join_with_or_without_slash(StorageFileField, '', methods=['GET'])
def index():
  abort(404)

# TODO: worry about permissioned access to `storage://`
# TODO: worry about access to `file://`
# TODO: worry about access to other providers via API as a proxy

@route_join_with_or_without_slash(StorageFileField, 'ls', methods=['GET'])
@route_join_with_or_without_slash(StorageFileField, 'ls', '<path:path>', methods=['GET'])
def ls(path=''):
  try:
    fs, fs_path = url_to_fs_ex(path + '#?' + request.query_string.decode())
    return jsonify(fs.ls(fs_path))
  except Exception as e:
    import traceback
    traceback.print_exc()
    abort(500)

@route_join_with_or_without_slash(StorageFileField, 'info', methods=['GET'])
@route_join_with_or_without_slash(StorageFileField, 'info', '<path:path>', methods=['GET'])
def info(path=''):
  try:
    fs, fs_path = url_to_fs_ex(path + '#?' + request.query_string.decode())
    return jsonify(fs.info(fs_path))
  except Exception as e:
    import traceback
    traceback.print_exc()
    abort(500)

@route_join_with_or_without_slash(StorageFileField, 'cat', methods=['GET'])
@route_join_with_or_without_slash(StorageFileField, 'cat', '<path:path>', methods=['GET'])
def cat(path=''):
  try:
    fs, fs_path = url_to_fs_ex(path + '#?' + request.query_string.decode())
    return fs.cat(fs_path)
  except Exception as e:
    import traceback
    traceback.print_exc()
    abort(500)

@route_join_with_or_without_slash(StorageFileField, 'read_block', methods=['GET'])
@route_join_with_or_without_slash(StorageFileField, 'read_block', '<path:path>', methods=['GET'])
def read_block(path=''):
  try:
    m = re.match(r'^(bytes )?(\d+)-(\d+)$', request.headers['Range'])
    _, start, end = m.groups()
    fs, fs_path = url_to_fs_ex(path + '#?' + request.query_string.decode())
    return fs.read_block(fs_path, start, end - start)
  except Exception as e:
    import traceback
    traceback.print_exc()
    abort(500)
