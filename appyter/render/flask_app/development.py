from appyter.ext.asyncio.helpers import ensure_sync
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
    env=dict(os.environ),
  )

async def app_runner(emitter, config):
  import asyncio
  from appyter.ext.subprocess import interrupt
  state_lock = asyncio.Lock()
  state = dict(proc=await run_app(config))
  #
  @emitter.on('reload')
  async def reload(changes):
    logger.info(f"Reload {changes}")
    async with state_lock:
      if 'proc' in state:
        proc = state.pop('proc')
        interrupt(proc)
        state['proc'] = await run_app(config)
  #
  @emitter.on('quit')
  async def quit():
    logger.info('Stopping app..')
    async with state_lock:
      proc = state.pop('proc')
      interrupt(proc)

async def app_messager(emitter, config):
  import asyncio
  from appyter.ext.urllib import join_slash
  from appyter.ext.socketio import AsyncClient
  from appyter.ext.asyncio.try_n_times import async_try_n_times
  async with AsyncClient() as sio:
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
    await async_try_n_times(3, sio.connect, origin, socketio_path=path)
    await sio.wait()

async def file_watcher(emitter, evt, path, **kwargs):
  from watchgod import awatch
  logger.info(f"Watching {path} for {evt}...")
  async for changes in awatch(path, **kwargs):
    await emitter.emit(evt, changes=changes)

@ensure_sync
async def serve(app_path, **kwargs):
  import os
  import asyncio
  import appyter
  from appyter.ext.asyncio.event_emitter import EventEmitter
  from appyter.ext.watchgod.watcher import GlobWatcher
  from appyter.context import get_env
  config = get_env(**kwargs)
  emitter = EventEmitter()
  tasks = []
  # run the app and reload it when necessary
  tasks.append(asyncio.create_task(app_runner(emitter, config)))
  # the underlying appyter library
  tasks.append(asyncio.create_task(
    file_watcher(emitter, 'reload', appyter.__path__[0],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['*'],
        include_file_glob=['*.py'],
        exclude_dir_glob=[],
        exclude_file_glob=[],
      ),
    )
  ))
  # the underlying appyter library's templates/ipynb/staticfiles/...
  tasks.append(asyncio.create_task(
    file_watcher(emitter, 'livereload', appyter.__path__[0],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['*'],
        include_file_glob=['*'],
        exclude_dir_glob=[],
        exclude_file_glob=['*.py'],
      ),
    )
  ))
  # the appyter itself's filters/blueprints
  tasks.append(asyncio.create_task(
    file_watcher(emitter, 'reload', config['CWD'],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['filters', 'blueprints'],
        include_file_glob=['*.py'],
        exclude_dir_glob=[],
        exclude_file_glob=[],
      ),
    )
  ))
  # the appyter itself's templates/ipynb/staticfiles/...
  tasks.append(asyncio.create_task(
    file_watcher(emitter, 'livereload', config['CWD'],
      watcher_cls=GlobWatcher,
      watcher_kwargs=dict(
        include_dir_glob=['*'],
        include_file_glob=['*'],
        exclude_dir_glob=[config['DATA_DIR']],
        exclude_file_glob=['*.py'],
      ),
    )
  ))
  tasks.append(asyncio.create_task(app_messager(emitter, config)))
  exit_code = 0
  try:
    await asyncio.Event().wait()
  except asyncio.CancelledError:
    pass
  except:
    exit_code = 1
  finally:
    await emitter.emit('quit')
    await emitter.flush()
    await emitter.clear()
    for task in tasks:
      try:
        task.cancel()
        await task
      except asyncio.CancelledError:
        pass
  return exit_code
