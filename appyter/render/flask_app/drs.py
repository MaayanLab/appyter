'''
A DRS endpoint for accessing `storage://input`
'''

import re
import datetime as dt
import logging
logger = logging.getLogger(__name__)

from flask import current_app, request, send_file, abort
from appyter.render.flask_app.core import core
from appyter.render.flask_app.constants import get_input_fs
from appyter.ext.urllib import url_filename
from appyter import __version__

@core.route('/ga4gh/drs/v1/service-info', methods=['GET'])
def drs_service_info():
  from pathlib import PurePath
  from appyter.ext.re import slugify
  name = slugify(PurePath(current_app.config['IPYNB']).stem.lower())
  return {
    'id': f"cloud.maayanlab.appyter.{name}",
    'name': 'Appyter',
    'type': {
      'group': 'cloud.maayanlab.appyter',
      'artifact': 'drs',
      'version': '1.0.0',
    },
    'organization': {
      'name': 'MaayanLab',
      'url': 'https://maayanlab.cloud',
    },
    'version': __version__,
  }

@core.route('/ga4gh/drs/v1/objects/<string:file_id>', methods=['GET'])
def drs_objects(file_id):
  try:
    fs = get_input_fs()
    file_info = fs.info(file_id)
    assert file_info['type'] == 'file', 'NotAFile'
  except:
    return abort(404)
  #
  res = {
    'id': file_id,
    'self_uri': f"{re.sub(r'^https?://', 'drs://', (current_app.config.get('PUBLIC_URL') or request.url_root).strip('/'))}/{file_id}",
    'access_methods': [
      {
        'access_id': 'primary',
        'type': 'https',
      },
    ],
    'checksums': [
      {
        'type': 'sha-1',
        'checksum': file_id,
      }
    ],
    'created_time': (
      dt.datetime.fromtimestamp(file_info['created'])
      if 'created' in file_info else
      dt.datetime.now()
    ).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'size': file_info['size'],
  }
  return res

@core.route('/ga4gh/drs/v1/objects/<string:file_id>/access/<string:access_id>', methods=['GET'])
def drs_objects_access(file_id, access_id):
  if access_id != 'primary':
    return abort(404)
  #
  try:
    fs = get_input_fs()
    file_info = fs.info(file_id)
    assert file_info['type'] == 'file', 'NotAFile'
  except:
    return abort(404)
  #
  return {
    'url': f"{(current_app.config.get('PUBLIC_URL') or request.url_root).strip('/')}/ga4gh/drs/v1/objects/{file_id}/fetch",
  }

@core.route('/ga4gh/drs/v1/objects/<string:file_id>/fetch', methods=['GET'])
def drs_objects_fetch(file_id):
  try:
    fs = get_input_fs()
    file_info = fs.info(file_id)
    assert file_info['type'] == 'file', 'NotAFile'
  except:
    return abort(404)
  #
  return send_file(fs.open(file_info['name'], 'rb'), attachment_filename=url_filename(file_info['name']))
