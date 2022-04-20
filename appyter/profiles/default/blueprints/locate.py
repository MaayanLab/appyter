import logging

from appyter.render.flask_app.prepare import prepare_request
logger = logging.getLogger(__name__)

def locate(flask_app, url_prefix=None):
  if 'catalog-integration' in flask_app.config['EXTRAS']:
    logger.info("Enabling locate blueprint...")

    from flask import Blueprint, abort, jsonify, request
    import traceback
    from appyter.ext.flask import route_join_with_or_without_slash
    from appyter.extras.catalog_integration.userfs import create_userfs
    from appyter.ext.asyncio.helpers import ensure_sync

    blueprint = Blueprint('locate', __name__)

    @route_join_with_or_without_slash(blueprint, '', methods=['GET'])
    def index():
      abort(404)

    @route_join_with_or_without_slash(blueprint, 'ls', methods=['GET'])
    @route_join_with_or_without_slash(blueprint, 'ls', '<path:path>', methods=['GET'])
    def ls(path=''):
      if not path.startswith('user://'):
        return abort(404)
      try:
        data = prepare_request(request)
        user_fs = ensure_sync(create_userfs(data))
      except:
        logger.error(traceback.format_exc())
        return abort(401)
      try:
        with user_fs as user_fs:
          return jsonify(user_fs.ls(path[len('user://'):], detail=True))
      except KeyboardInterrupt:
        raise
      except Exception:
        logger.error(traceback.format_exc())
        return abort(500)

    flask_app.register_blueprint(blueprint, url_prefix=url_prefix)
