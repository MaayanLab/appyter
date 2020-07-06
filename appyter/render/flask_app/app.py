import os
import click
import uuid
from flask import Flask, Blueprint, current_app
from flask.cli import with_appcontext, run_command

from appyter.render.flask_app.socketio import socketio, emit
from appyter.render.flask_app.core import core
import appyter.render.flask_app.download
import appyter.render.flask_app.execution

from appyter.cli import cli
from appyter.context import get_env, get_extra_files, find_blueprints
from appyter.util import join_routes

def create_app(**kwargs):
  ''' Completely initialize the flask application
  '''
  config = get_env(**kwargs)
  #
  print('Initializing flask...')
  app = Flask(__name__, static_url_path=config['STATIC_PREFIX'], static_folder=config['STATIC_DIR'])
  app.config.update(config)
  app.debug = config['DEBUG']
  #
  if app.config['PROXY']:
    print('wsgi proxy fix...')
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
  #
  print('Preparing data directory...')
  os.makedirs(app.config['DATA_DIR'], exist_ok=True)
  #
  print('Registering blueprints...')
  app.register_blueprint(core, url_prefix=app.config['PREFIX'])
  for blueprint_name, blueprint in find_blueprints(config=app.config).items():
    if isinstance(blueprint, Blueprint):
      app.register_blueprint(blueprint, url_prefix=join_routes(app.config['PREFIX'], blueprint_name))
    elif callable(blueprint):
      blueprint(app, url_prefix=join_routes(app.config['PREFIX'], blueprint_name), DATA_DIR=app.config['DATA_DIR'])
    else:
      raise Exception('Unrecognized blueprint type: ' + blueprint_name)
  #
  print('Initializing socketio...')
  socketio.init_app(app, 
    path=f"{app.config['PREFIX']}socket.io",
    async_mode='threading' if app.config['DEBUG'] else 'eventlet',
    logger=bool(app.config['DEBUG']),
    engineio_logger=bool(app.config['DEBUG']),
    cors_allowed_origins='*',
  )
  #
  return app

# register flask_app with CLI
@cli.group(invoke_without_command=True)
@click.option('--cwd', envvar='CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click.option('--prefix', envvar='PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click.option('--profile', envvar='PROFILE', default='default', help='Specify the profile to use for rendering')
@click.option('--host', envvar='HOST', default='127.0.0.1', help='The host the flask server should run on')
@click.option('--port', envvar='PORT', type=int, default=5000, help='The port this flask server should run on')
@click.option('--proxy', envvar='PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click.option('--data-dir', envvar='DATA_DIR', default='data', help='The directory to store data of executions')
@click.option('--max-threads', envvar='MAX_THREADS', type=int, default=10, help='The number of worker threads')
@click.option('--secret-key', envvar='SECRET_KEY', default=str(uuid.uuid4()), help='A secret key for flask')
@click.option('--debug', envvar='DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
@click.option('--static-dir', envvar='STATIC_DIR', default='static', help='The folder whether staticfiles are located')
@click.argument('ipynb', envvar='IPYNB')
@click.pass_context
def flask_app(ctx, *args, **kwargs):
  if ctx.invoked_subcommand is None:
    return ctx.forward(run, *args, **kwargs)

@flask_app.command()
def run(*args, **kwargs):
  if not kwargs.get('debug'):
    print('Patching...')
    import eventlet
    eventlet.monkey_patch()
  #
  app = create_app(**kwargs)
  return socketio.run(
    app,
    host=app.config['HOST'],
    port=app.config['PORT'],
    debug=app.config['DEBUG'],
    use_reloader=app.config['DEBUG'],
    extra_files=get_extra_files(config=app.config),
  )
