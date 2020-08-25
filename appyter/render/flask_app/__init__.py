import os
import uuid
import click
import logging
logger = logging.getLogger(__name__)

from appyter.cli import cli
from appyter.util import click_option_setenv, click_argument_setenv
# from appyter.ext.flask_aiohttp import AioHTTP

def create_app(**kwargs):
  ''' Completely initialize the flask application
  '''
  from aiohttp import web
  from aiohttp_wsgi import WSGIHandler
  #
  from flask import Flask, Blueprint, current_app
  from flask_cors import CORS
  #
  from appyter.render.flask_app.socketio import socketio
  from appyter.render.flask_app.core import core
  import appyter.render.flask_app.static
  import appyter.render.flask_app.download
  import appyter.render.flask_app.execution
  #
  from appyter.context import get_env, find_blueprints
  from appyter.util import join_routes
  config = get_env(**kwargs)
  #
  if config['DEBUG']:
    logging.basicConfig(level=logging.DEBUG)
  #
  logger.info('Initializing aiohttp...')
  app = web.Application()
  app['config'] = config
  #
  logger.info('Initializing socketio...')
  socketio.attach(app)
  #
  logger.info('Initializing flask...')
  flask_app = Flask(__name__, static_url_path=None, static_folder=None)
  CORS(flask_app)
  flask_app.config.update(config)
  flask_app.debug = config['DEBUG']
  #
  if flask_app.config['PROXY']:
    logger.info('wsgi proxy fix...')
    from werkzeug.middleware.proxy_fix import ProxyFix
    flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1, x_proto=1)
  #
  logger.info('Registering blueprints...')
  flask_app.register_blueprint(core, url_prefix=flask_app.config['PREFIX'])
  for blueprint_name, blueprint in find_blueprints(config=flask_app.config).items():
    if isinstance(blueprint, Blueprint):
      flask_app.register_blueprint(blueprint, url_prefix=join_routes(flask_app.config['PREFIX'], blueprint_name))
    elif callable(blueprint):
      blueprint(flask_app, url_prefix=join_routes(flask_app.config['PREFIX'], blueprint_name), DATA_DIR=flask_app.config['DATA_DIR'])
    else:
      raise Exception('Unrecognized blueprint type: ' + blueprint_name)
  #
  logger.info('Registering flask with aiohttp...')
  wsgi_handler = WSGIHandler(flask_app)
  app.router.add_route('*', '/{path_info:.*}', wsgi_handler)
  return app

# register flask_app with CLI
@cli.command(help='Run a flask web application based on an appyter-enabled jupyter notebook')
@click_option_setenv('--cwd', envvar='CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_option_setenv('--prefix', envvar='PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click_option_setenv('--profile', envvar='PROFILE', default='default', help='Specify the profile to use for rendering')
@click_option_setenv('--extras', envvar='EXTRAS', default=[], type=str, multiple=True, help='Specify extras flags')
@click_option_setenv('--host', envvar='HOST', default='127.0.0.1', help='The host the flask server should run on')
@click_option_setenv('--port', envvar='PORT', type=int, default=5000, help='The port this flask server should run on')
@click_option_setenv('--proxy', envvar='PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click_option_setenv('--data-dir', envvar='DATA_DIR', default='data', help='The directory to store data of executions')
@click_option_setenv('--dispatcher', envvar='DISPATCHER', type=str, help='The URL to the dispatcher, otherwise use an embedded dispatcher')
@click_option_setenv('--secret-key', envvar='SECRET_KEY', default=str(uuid.uuid4()), help='A secret key for flask')
@click_option_setenv('--debug', envvar='DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
@click_option_setenv('--static-dir', envvar='STATIC_DIR', default='static', help='The folder whether staticfiles are located')
@click_option_setenv('--keyfile', envvar='KEYFILE', default=None, help='The SSL certificate private key for wss support')
@click_option_setenv('--certfile', envvar='CERTFILE', default=None, help='The SSL certificate public key for wss support')
@click_argument_setenv('ipynb', envvar='IPYNB')
def flask_app(**kwargs):
  # write all config to env
  if kwargs.get('debug'):
    from aiohttp_devtools.logs import setup_logging
    from aiohttp_devtools.runserver import runserver, run_app
    setup_logging(True)
    run_app(*runserver(app_path=__file__))
  else:
    from aiohttp import web
    app = create_app(**kwargs)
    return web.run_app(app)
