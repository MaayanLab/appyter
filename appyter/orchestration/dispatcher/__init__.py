import click
from appyter.orchestration.cli import orchestration

def create_app(**kwargs):
  from flask import Flask
  from appyter.orchestration.dispatcher.socketio import socketio
  from appyter.orchestration.dispatcher.core import core
  print('Initializing flask...')
  app = Flask(__name__)
  app.config.update(dict(
    HOST=kwargs.get('host'),
    PORT=kwargs.get('port'),
    PROXY=kwargs.get('proxy'),
    JOBS=kwargs.get('jobs'),
    DEBUG=kwargs.get('debug'),
    PREFIX=kwargs.get('prefix'),
    DISPATCH=kwargs.get('dispatch'),
  ))
  if app.config['PROXY']:
    print('wsgi proxy fix...')
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
  app.register_blueprint(core, url_prefix=app.config['PREFIX'])
  print('Initializing socketio...')
  socketio.init_app(app,
    path=f"{app.config['PREFIX']}socket.io",
    async_mode='threading' if app.config['DEBUG'] else 'eventlet',
    logger=bool(app.config['DEBUG']),
    engineio_logger=bool(app.config['DEBUG']),
    cors_allowed_origins='*',
  )
  return app

@orchestration.command(help='Run the appyter dispatcher')
@click.option('--prefix', envvar='PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click.option('--host', envvar='HOST', default='127.0.0.1', help='The host the flask server should run on')
@click.option('--port', envvar='PORT', type=int, default=5000, help='The port this flask server should run on')
@click.option('--proxy', envvar='PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click.option('--jobs', envvar='JOBS', type=int, default=1, help='Number of concurrent jobs to dispatch')
@click.option('--debug', envvar='DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
@click.option('--dispatch', envvar='DISPATCH', type=str, default='native', help='The dispatcher mechanism to use (see list-dispatchers)')
def dispatcher(*args, **kwargs):
  from appyter.orchestration.dispatcher.socketio import socketio
  from appyter.util import dict_filter_none
  #
  run_args = dict()
  app = create_app(**kwargs)
  run_args.update(
    host=app.config['HOST'],
    port=app.config['PORT'],
    debug=app.config['DEBUG'],
  )
  return socketio.run(app, **dict_filter_none(run_args))