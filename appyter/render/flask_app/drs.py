'''
A DRS endpoint which supports arbitrary serialized fsspec uris.
The id is a HS256 encrypted JWT with the actual json of the form
`{ "fs": { fsspec_serialized }, "fo": "path" }`
The encrypted JWT allows us to not have to worry about sensitive credentials
  in the file storage spec and also ensures we won't receive untrusted input
  which would otherwise open this endpoint to XSS vulnerabilities.
'''

import re
import traceback
import contextlib
import datetime as dt
import logging

logger = logging.getLogger(__name__)
from flask import current_app, send_file, abort
from appyter.ext.fsspec.spec.composable import ComposableAbstractFileSystem
from appyter.render.flask_app.core import core
from appyter.ext.hashlib import hashsum_io
from appyter.ext.urllib import url_filename


@contextlib.contextmanager
def parse_id(id):
  import json
  from jwcrypto import jwk, jwe
  logger.info(f"DRS Parsing {id=}")
  try:
    key = jwk.JWK.from_json(json.dumps({ 'kty': 'oct', 'k': current_app.config['SECRET_KEY'] }))
    jwetoken = jwe.JWE()
    jwetoken.deserialize(id)
    jwetoken.decrypt(key)
    payload = json.loads(jwetoken.payload)
  except:
    logger.warning(traceback.format_exc())
    abort(404)
  #
  try:
    fs, fo = ComposableAbstractFileSystem.from_json(json.dumps(payload['fs'])), payload['fo']
  except KeyError:
    logger.warning(traceback.format_exc())
    abort(400)
  except:
    logger.error(traceback.format_exc())
    abort(500)
  #
  if getattr(fs, '__enter__', None):
    fs.__enter__()
  try:
    file_info = fs.info(fo)
  except FileNotFoundError:
    logger.warning(traceback.format_exc())
    return abort(404)
  try:
    yield fs, file_info
  finally:
    if getattr(fs, '__exit__', None):
      import sys
      fs.__exit__(*sys.exc_info())

@core.route('/ga4gh/v1/objects/<string:id>', methods=['GET'])
def drs_objects(id):
  with parse_id(id) as (fs, file_info):
    logger.info(f"{file_info=}")
    if file_info['type'] != 'file': return abort(404)
    # TODO: hash calculation here is likely expensive..
    with fs.open(file_info['name'], 'rb') as fr:
      sha256 = hashsum_io('sha256', fr)
    res = {
      'id': id,
      'self_uri': f"{re.sub(r'^https?://', 'drs://', current_app.config['PUBLIC_URL'])}/{id}",
      'access_methods': [
        {
          # TODO: this can be a last resort but in certain circumstances we should
          #       be able to passthrough the underlying provider (like s3 or whatnot)
          'type': 'https',
          'access_url': {
            'url': f"{current_app.config['PUBLIC_URL']}/ga4gh/v1/objects/{id}/fetch",
          },
        },
      ],
      'checksums': [
        {
          'type': 'sha-256',
          'checksum': sha256,
        }
      ],
      'created_time': (
        dt.datetime.from_timestamp(file_info['created'])
        if 'created' in file_info else
        dt.datetime.now()
      ).strftime('%Y-%m-%dT%H:%M:%SZ'),
      'size': file_info['size'],
    }
    logger.info(f"{res=}")
    return res

@core.route('/ga4gh/v1/objects/<string:id>/fetch', methods=['GET'])
def drs_object_fetch(id):
  with parse_id(id) as (fs, file_info):
    if file_info['type'] != 'file': return abort(404)
    return send_file(fs.open(file_info['name'], 'rb'), attachment_filename=url_filename(file_info['name']))
