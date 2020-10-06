import click
from appyter.orchestration.cli import orchestration

def create_app(**kwargs):
  import logging
  from flask import Flask
  from appyter.orchestration.dispatcher.socketio import socketio
  from appyter.orchestration.dispatcher.core import core
  from appyter.util import join_routes
  logger = logging.getLogger(__name__)
  logging.basicConfig(level=logging.DEBUG if kwargs.get('debug') else logging.WARNING)
  logger.info('Initializing flask...')
  app = Flask(__name__)
  app.config.update(dict(
    HOST=kwargs.get('host'),
    PORT=kwargs.get('port'),
    PROXY=kwargs.get('proxy'),
    JOBS=kwargs.get('jobs'),
    JOBS_PER_IMAGE=kwargs.get('jobs_per_image'),
    DEBUG=kwargs.get('debug'),
    PREFIX=kwargs.get('prefix'),
    KUBE_NAMESPACE=kwargs.get('kube_namespace'),
    DISPATCH=kwargs.get('dispatch'),
  ))
  if app.config['PROXY']:
    logger.info('wsgi proxy fix...')
    from werkzeug.middleware.proxy_fix import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)
  app.register_blueprint(core, url_prefix=app.config['PREFIX'])
  logger.info('Initializing socketio...')
  socketio.init_app(app,
    path=join_routes(app.config['PREFIX'], 'socket.io'),
    async_mode='threading',
    logger=bool(app.config['DEBUG']),
    engineio_logger=bool(app.config['DEBUG']),
    cors_allowed_origins='*',
  )
  return app

@orchestration.command(help='Run the appyter dispatcher')
@click.option('--prefix', envvar='APPYTER_PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click.option('--host', envvar='APPYTER_HOST', default='127.0.0.1', help='The host the flask server should run on')
@click.option('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this flask server should run on')
@click.option('--proxy', envvar='APPYTER_PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click.option('--jobs', envvar='APPYTER_JOBS', type=int, default=2, help='Number of concurrent jobs to dispatch')
@click.option('--jobs-per-image', envvar='APPYTER_JOBS_PER_IMAGE', type=int, default=1, help='Number of concurrent jobs to dispatch for any individual appyter image')
@click.option('--debug', envvar='APPYTER_DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
@click.option('--kube-namespace', envvar='APPYTER_KUBE_NAMESPACE', type=str, default='default', help='The kubernetes namespace (kubernetes dispatch)')
@click.option('--dispatch', envvar='APPYTER_DISPATCH', type=str, default='native', help='The dispatcher mechanism to use (see list-dispatchers)')
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
