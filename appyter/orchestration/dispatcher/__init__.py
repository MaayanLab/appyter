import click
import logging
logger = logging.getLogger(__name__)

from appyter.orchestration.cli import orchestration
from appyter.ext.click import click_option_setenv


def create_app(**kwargs):
  from aiohttp import web
  #
  from appyter.orchestration.dispatcher.core import core
  from appyter.orchestration.dispatcher.socketio import socketio
  from appyter.util import join_routes
  #
  logging.basicConfig(
    level=logging.DEBUG if kwargs.get('debug') else logging.WARNING,
    format='%(name)s %(message).80s',
  )
  #
  logger.info('Initializing aiohttp...')
  config = dict(
    HOST=kwargs.get('host'),
    PORT=kwargs.get('port'),
    PROXY=kwargs.get('proxy'),
    JOBS=kwargs.get('jobs'),
    JOBS_PER_IMAGE=kwargs.get('jobs_per_image'),
    DEBUG=kwargs.get('debug'),
    PREFIX=kwargs.get('prefix'),
    KUBE_NAMESPACE=kwargs.get('kube_namespace'),
    DISPATCH=kwargs.get('dispatch'),
  )
  if config['PREFIX'].rstrip('/'):
    app = web.Application()
    app['config'] = core['config'] = config
    #
    logger.info('Registering prefix redirect')
    async def redirect_to_prefix(request):
      path = request.match_info['path']
      raise web.HTTPFound(join_routes(app['config']['PREFIX'], path) + '/')
    app.router.add_get('/{path:[^/]*}', redirect_to_prefix)
    app.add_subapp(config['PREFIX'].rstrip('/'), core)
  else:
    app = core
    app['config'] = config
  #
  logger.info('Initializing socketio...')
  socketio.attach(app, join_routes(app['config']['PREFIX'], 'socket.io'))
  #
  return app

@orchestration.command(help='Run the appyter dispatcher')
@click_option_setenv('--prefix', envvar='APPYTER_PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click_option_setenv('--host', envvar='APPYTER_HOST', default='127.0.0.1', help='The host the flask server should run on')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this flask server should run on')
@click_option_setenv('--proxy', envvar='APPYTER_PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click_option_setenv('--jobs', envvar='APPYTER_JOBS', type=int, default=2, help='Number of concurrent jobs to dispatch')
@click_option_setenv('--jobs-per-image', envvar='APPYTER_JOBS_PER_IMAGE', type=int, default=1, help='Number of concurrent jobs to dispatch for any individual appyter image')
@click_option_setenv('--debug', envvar='APPYTER_DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
@click_option_setenv('--kube-namespace', envvar='APPYTER_KUBE_NAMESPACE', type=str, default='default', help='The kubernetes namespace (kubernetes dispatch)')
@click_option_setenv('--dispatch', envvar='APPYTER_DISPATCH', type=str, default='native', help='The dispatcher mechanism to use (see list-dispatchers)')
def dispatcher(*args, **kwargs):
  from aiohttp import web
  from appyter.orchestration.dispatcher.socketio import socketio
  from appyter.util import dict_filter_none
  #
  app = create_app(**kwargs)
  web.run_app(app, host=app['config']['HOST'], port=int(app['config']['PORT']))
