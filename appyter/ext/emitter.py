import contextlib
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
    from appyter.ext.socketio import AsyncClient
    import urllib.parse
    async with AsyncClient() as sio:
      url_parsed = urllib.parse.urlparse(url)
      url_path, room = url_parsed.path.rsplit('/', maxsplit=1)
      await sio.connect(f"{url_parsed.scheme}://{url_parsed.netloc}", socketio_path=url_path)
      await sio.emit('join', room)
      async def emit(msg):
        await sio.emit('forward', dict(event=msg['type'], data=msg['data'], to=room))
      try:
        yield emit
      finally:
        await sio.disconnect()
  else:
    raise NotImplementedError
