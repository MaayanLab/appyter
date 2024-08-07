import logging
logger = logging.getLogger(__name__)

from appyter.orchestration.cli import orchestration
from appyter.ext.click import click_option_setenv


def create_app(**kwargs):
  from aiohttp import web
  #
  from appyter.orchestration.dispatcher.core import core
  from appyter.orchestration.dispatcher.socketio import socketio
  from appyter.ext.urllib import join_slash
  #
  logger.info('Initializing aiohttp...')
  config = dict(
    HOST=kwargs.get('host'),
    PORT=kwargs.get('port'),
    PROXY=kwargs.get('proxy'),
    JOBS=kwargs.get('jobs'),
    JOBS_PER_IMAGE=kwargs.get('jobs_per_image'),
    TIMEOUT=kwargs.get('timeout'),
    DEBUG=kwargs.get('debug'),
    PREFIX=kwargs.get('prefix', '').rstrip('/'),
  )
  if config['PREFIX']:
    app = web.Application()
    app['config'] = core['config'] = config
    #
    logger.info('Registering prefix redirect')
    async def redirect_to_prefix(request):
      path = request.match_info['path']
      raise web.HTTPFound(join_slash(app['config']['PREFIX'], path) + '/')
    app.router.add_get('/{path:[^/]*}', redirect_to_prefix)
    app.add_subapp(config['PREFIX'], core)
  else:
    app = core
    app['config'] = config
  #
  logger.info('Initializing socketio...')
  socketio.attach(app, join_slash(app['config']['PREFIX'], 'socket.io'))
  #
  return app

@orchestration.command(help='Run the appyter dispatcher')
@click_option_setenv('--prefix', envvar='APPYTER_PREFIX', default='/', help='Specify the prefix for which to mount the webserver onto')
@click_option_setenv('--host', envvar='APPYTER_HOST', default='127.0.0.1', help='The host the flask server should run on')
@click_option_setenv('--port', envvar='APPYTER_PORT', type=int, default=5000, help='The port this flask server should run on')
@click_option_setenv('--proxy', envvar='APPYTER_PROXY', type=bool, default=False, help='Whether this is running behind a proxy and the IP should be fixed for CORS')
@click_option_setenv('--jobs', envvar='APPYTER_JOBS', type=int, default=2, help='Number of concurrent jobs to dispatch')
@click_option_setenv('--jobs-per-image', envvar='APPYTER_JOBS_PER_IMAGE', type=int, default=1, help='Number of concurrent jobs to dispatch for any individual appyter image')
@click_option_setenv('--timeout', envvar='APPYTER_TIMEOUT', type=float, default=None, help='How long in seconds a job can run before it is cancelled')
@click_option_setenv('--debug', envvar='APPYTER_DEBUG', type=bool, default=True, help='Whether or not we should be in debugging mode, not for use in multi-tenant situations')
def dispatcher(*args, **kwargs):
  from appyter.ext.aiohttp import run_app
  from appyter.ext.asyncio.event_loop import with_event_loop
  with with_event_loop():
    app = create_app(**kwargs)
    run_app(app, host=app['config']['HOST'], port=int(app['config']['PORT']))
