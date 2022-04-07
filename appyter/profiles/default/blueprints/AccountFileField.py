'''
WARNING: This blueprint may open an XSS vulnerability, and is thus opt-in through the storage-file-field extra, use with caution.
'''
import logging
logger = logging.getLogger(__name__)

def AccountFileField(flask_app, url_prefix=None):
  if 'catalog-integration' in flask_app.config['EXTRAS']:
    logger.info("Enabling account file field...")

    from flask import Blueprint, abort, jsonify, request
    import traceback
    from appyter.ext.fsspec.core import url_to_fs_ex
    from appyter.ext.flask import route_join_with_or_without_slash

    blueprint = Blueprint('AccountFileField', __name__)

    @route_join_with_or_without_slash(blueprint, '', methods=['GET'])
    def index():
      abort(404)

    @route_join_with_or_without_slash(blueprint, 'ls', methods=['GET'])
    @route_join_with_or_without_slash(blueprint, 'ls', '<path:path>', methods=['GET'])
    def ls(path=''):
      try:
        assert path.startswith('catalog://')
        fs, fs_path = url_to_fs_ex(path + '#?' + request.query_string.decode())
        return jsonify(fs.ls(fs_path))
      except KeyboardInterrupt:
        raise
      except Exception:
        logger.error(traceback.format_exc())
        abort(500)

    @route_join_with_or_without_slash(blueprint, 'info', methods=['GET'])
    @route_join_with_or_without_slash(blueprint, 'info', '<path:path>', methods=['GET'])
    def info(path=''):
      try:
        assert path.startswith('catalog://')
        fs, fs_path = url_to_fs_ex(path + '#?' + request.query_string.decode())
        return jsonify(fs.info(fs_path))
      except KeyboardInterrupt:
        raise
      except Exception:
        logger.error(traceback.format_exc())
        abort(500)

    flask_app.register_blueprint(blueprint, url_prefix=url_prefix)
