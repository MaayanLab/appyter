import contextlib
import traceback
import logging
logger = logging.getLogger(__name__)

def json_emitter_factory(output):
  async def json_emitter(obj):
    import json
    print(json.dumps(obj), file=output)
  return json_emitter

@contextlib.asynccontextmanager
async def url_to_emitter(url):
  if url.startswith('file://'):
    import fsspec
    with fsspec.open(url, 'w') as fw:
      yield json_emitter_factory(fw)
  elif url.startswith('http://') or url.startswith('https://'):
    import fsspec
    import urllib.parse
    from appyter.ext.socketio import AsyncClient
    with fsspec.open('file:///dev/stderr', 'w') as fw:
      fallback_emitter = json_emitter_factory(fw)
      async with AsyncClient() as sio:
        url_parsed = urllib.parse.urlparse(url)
        url_path, room = url_parsed.path.rsplit('/', maxsplit=1)
        try:
          await sio.connect(f"{url_parsed.scheme}://{url_parsed.netloc}", socketio_path=url_path)
        except:
          await fallback_emitter(dict(
            type='error',
            data=f"Failed to connect to {url}... falling back to stderr",
            traceback=traceback.format_exc(),
          ))
        else:
          try:
            await sio.emit('join', room)
          except:
            await fallback_emitter(dict(
              type='error',
              data=f"Failed to join {room}...",
              traceback=traceback.format_exc(),
            ))
        async def emit(msg):
          try:
            await sio.emit(msg['type'], msg['data'], to=room)
          except:
            await fallback_emitter(dict(msg,
              traceback=traceback.format_exc(),
            ))
        try:
          yield emit
        finally:
          try:
            await sio.disconnect()
          except:
            await fallback_emitter(dict(
              type='error',
              data=f"Failed to disconnect.",
              traceback=traceback.format_exc(),
            ))
  else:
    logger.error("Emitter not recognized, falling back to stderr")
    import fsspec
    with fsspec.open('file:///dev/stderr', 'w') as fw:
      yield json_emitter_factory(fw)
