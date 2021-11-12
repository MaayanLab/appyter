import logging
logger = logging.getLogger(__name__)

async def run_app(config):
  import os
  import sys
  import asyncio
  return await asyncio.create_subprocess_exec(
    sys.executable, '-u', '-m', 'appyter',
    f"--socket={config['HOST']}:{config['PORT']}",
    stdout=sys.stdout,
    stderr=sys.stderr,
    env=os.environ,
  )

async def app_runner(emitter, config):
  import asyncio
  state_lock = asyncio.Lock()
  state = dict(proc=await run_app(config))
  #
  @emitter.on('reload')
  async def reload(changes):
    logger.info(f"Reload {changes}")
    async with state_lock:
      if 'proc' in state:
        proc = state.pop('proc')
        proc.kill()
        state['proc'] = await run_app(config)
  #
  @emitter.on('quit')
  async def quit():
    logger.info('Stopping app..')
    async with state_lock:
      state.pop('proc').kill()

async def app_messager(emitter, config):
  import asyncio
  from appyter.ext.urllib import join_slash
  from appyter.ext.socketio import AsyncClient
  from appyter.ext.asyncio.try_n_times import try_n_times
  sio = AsyncClient()
  #
  @emitter.on('livereload')
  async def livereload(changes):
    logger.info(f"LiveReload {changes}")
    await sio.emit('livereload', {})
  #
  @emitter.on('quit')
  async def quit():
    logger.info('Disconnecting..')
    await sio.disconnect()
  #
  origin = f"http://{config['HOST']}:{config['PORT']}"
  path = join_slash(config['PREFIX'], "socket.io")
  logger.info(f"Connecting to appyter server at {origin}{path}...")
  await asyncio.sleep(1)
  await try_n_times(3, sio.connect, origin, socketio_path=path)
  await sio.wait()

async def file_watcher(emitter, evt, path, **kwargs):
  from watchgod import awatch
  logger.info(f"Watching {path} for {evt}...")
  async for changes in awatch(path, **kwargs):
    await emitter.emit(evt, changes=changes)

def serve(app_path, **kwargs):
  import os
  import asyncio
  import appyter
  from appyter.ext.asyncio.event_emitter import EventEmitter
  from appyter.ext.watchgod.watcher import GlobWatcher
  from appyter.context import get_env
  config = get_env(**kwargs)
  loop = asyncio.get_event_loop()
  emitter = EventEmitter()
  # run the app and reload it when necessary
  loop.create_task(app_runner(emitter, config))
  # the underlying appyter library
  loop.create_task(
    file_watcher(emitter, 'reload', appyter.__path__[0],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['*'],
        include_file_glob=['*.py'],
        exclude_dir_glob=[],
        exclude_file_glob=[],
      ),
    )
  )
  # the underlying appyter library's templates/ipynb/staticfiles/...
  loop.create_task(
    file_watcher(emitter, 'livereload', os.path.join(appyter.__path__[0], 'profiles'),
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['*'],
        include_file_glob=['*'],
        exclude_dir_glob=[],
        exclude_file_glob=['*.py'],
      ),
    )
  )
  # the appyter itself's filters/blueprints
  loop.create_task(
    file_watcher(emitter, 'reload', config['CWD'],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['filters', 'blueprints'],
        include_file_glob=['*.py'],
        exclude_dir_glob=[],
        exclude_file_glob=[],
      ),
    )
  )
  # the appyter itself's templates/ipynb/staticfiles/...
  loop.create_task(
    file_watcher(emitter, 'livereload', config['CWD'],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['*'],
        include_file_glob=['*'],
        exclude_dir_glob=[config['DATA_DIR']],
        exclude_file_glob=['*.py'],
      ),
    )
  )
  loop.create_task(app_messager(emitter, config))
  loop.run_forever()
  loop.run_until_complete(emitter.emit('quit'))
  loop.run_until_complete(emitter.flush())
  loop.run_until_complete(emitter.clear())
