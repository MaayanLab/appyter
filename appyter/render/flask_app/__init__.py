import os
import logging
import traceback
logger = logging.getLogger(__name__)

from appyter.cli import cli
from appyter.ext.click import Json, click_option_setenv, click_argument_setenv

def create_app(**kwargs):
  ''' Completely initialize the flask application
  '''
  import asyncio
  from aiohttp import web
  from aiohttp_wsgi import WSGIHandler
  from aiohttp_remotes import setup, XForwardedRelaxed
  from aiohttp.web_exceptions import HTTPException
  from aiohttp.web_middlewares import middleware
  #
  from flask import Flask, Blueprint
  from flask_cors import CORS
  #
  from appyter.render.flask_app.socketio import socketio
  from appyter.render.flask_app.core import core
  import appyter.render.flask_app.static
  import appyter.render.flask_app.export
  import appyter.render.flask_app.upload
  import appyter.render.flask_app.execution
  import appyter.render.flask_app.room_manager
  import appyter.render.flask_app.drs
  if kwargs['debug']:
    import appyter.render.flask_app.livereload
  #
  from appyter.context import get_env, find_blueprints
  from appyter.ext.urllib import join_slash
  from appyter.ext.flask import join_routes
  from appyter.ext.asyncio.helpers import ensure_async, ensure_sync
  config = get_env(**kwargs)
  #
  logger.info('Initializing aiohttp...')
  app = web.Application()
  app['config'] = config
  #
  if config['DEBUG']:
    logger.info('Initializing error handler middleware...')
    @middleware
    async def error_handler(request, handler):
      try:
        return await handler(request)
      except asyncio.CancelledError:
        raise
      except HTTPException:
        raise
      except Exception:
        logger.error(traceback.format_exc())
        await asyncio.sleep(1)
        raise web.HTTPFound(location=request.url)
    app.middlewares.append(error_handler)
  #
  logger.info('Initializing socketio...')
  socketio.attach(app, join_slash(config['PREFIX'], 'socket.io'))
  @app.cleanup_ctx.append
  async def initialize_socketio(app):
    async with socketio:
      yield
  #
  logger.info('Initializing flask...')
  flask_app = Flask(__name__, static_url_path=None, static_folder=None)
  CORS(flask_app)
  flask_app.config.update(config)
  flask_app.debug = config['DEBUG']
  #
  logger.info('Registering blueprints...')
  flask_app.register_blueprint(core)
  for blueprint_name, blueprint in find_blueprints(config=flask_app.config).items():
    if isinstance(blueprint, Blueprint):
      flask_app.register_blueprint(blueprint, url_prefix=join_routes(blueprint_name))
    elif callable(blueprint):
      blueprint(flask_app, url_prefix=join_routes(blueprint_name))
    else:
      raise Exception('Unrecognized blueprint type: ' + blueprint_name)
  #
  if app['config']['PREFIX'].strip('/'):
    logger.info('Registering prefix redirect')
    async def redirect_to_prefix(request):
      path = request.match_info['path']
      if path == app['config']['PREFIX'].strip('/'): path = ''
      raise web.HTTPFound(join_routes(app['config']['PREFIX'], path) + '/')
    app.router.add_get('/{path:[^/]*}', redirect_to_prefix)
  #
  logger.info('Registering flask with aiohttp...')
  wsgi_handler = WSGIHandler(flask_app)
  app.router.add_route('*', join_slash(app['config']['PREFIX'], '{path_info:.*}'), wsgi_handler)
  if flask_app.config['PROXY']:
    logger.info('Applying proxy fix middleware...')
    ensure_sync(setup(app, XForwardedRelaxed()))
  #
  async def storage_ctx(app):
    logger.info('Registering application storage handler')
    data_dir = app['config']['DATA_DIR']
    from appyter.ext.fsspec.storage import ensure_storage
    async with ensure_storage(data_dir) as fs:
      await ensure_async(fs.makedirs)('input', exist_ok=True)
      await ensure_async(fs.makedirs)('output', exist_ok=True)
      logger.info('Storage ready')
      yield
  app.cleanup_ctx.append(storage_ctx)
  #
  async def executor_ctx(app):
    logger.info('Registering application executor handler')
    executor_uri = app['config'].get('EXECUTOR') or 'local'
    from appyter.execspec.core import url_to_executor
    async with url_to_executor(executor_uri, config=app['config']) as executor:
      app['executor'] = executor
      logger.info('Executor ready')
      yield
  app.cleanup_ctx.append(executor_ctx)
  return app

# register flask_app with CLI
@cli.command(help='Run a flask web application based on an appyter-enabled jupyter notebook')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_option_setenv('--prefix', envvar='APPYTER_PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click_option_setenv('--profile', envvar='APPYTER_PROFILE', default='biojupies', help='Specify the profile to use for rendering')
@click_option_setenv('--extras', envvar='APPYTER_EXTRAS', default=[], type=Json(), multiple=True, help='Specify extras flags')
@click_option_setenv('--host', envvar='APPYTER_HOST', default='127.0.0.1', help='The host the flask server should run on')
@click_option_setenv('--socket', envvar='APPYTER_SOCKET', default=None, help='The socket to mount to (when running in production)')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this flask server should run on')
@click_option_setenv('--public-url', envvar='APPYTER_PUBLIC_URL', default=None, help='The public url users use to access the appyter (like when behind a load balancer)')
@click_option_setenv('--proxy', envvar='APPYTER_PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click_option_setenv('--data-dir', envvar='APPYTER_DATA_DIR', default='data', help='The directory to store data of executions')
@click_option_setenv('--executor', envvar='APPYTER_EXECUTOR', type=str, help='The executor URI which controls how executions are performed')
@click_option_setenv('--secret-key', envvar='APPYTER_SECRET_KEY', default=None, help='A secret key for flask')
@click_option_setenv('--debug', envvar='APPYTER_DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
@click_option_setenv('--static-dir', envvar='APPYTER_STATIC_DIR', default='static', help='The folder whether staticfiles are located')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def flask_app(**kwargs):
  import sys
  from appyter.ext.asyncio.event_loop import with_event_loop
  exit_code = 0
  try:
    with with_event_loop():
      if kwargs.get('socket'):
        from appyter.ext.aiohttp import run_app
        socket = kwargs['socket']
        logger.info(f"Launching aiohttp server on {socket}")
        app = create_app(**kwargs)
        if ':' in socket:
          host, port = socket.split(':')
          run_app(app, host=host, port=int(port))
        else:
          run_app(app, path=socket)
      elif kwargs.get('debug'):
        from appyter.render.flask_app.development import serve
        exit_code = serve(__file__, **kwargs)
      else:
        from appyter.render.flask_app.production import serve
        exit_code = serve(__file__, **kwargs)
  except KeyboardInterrupt:
    pass
  sys.exit(exit_code)
