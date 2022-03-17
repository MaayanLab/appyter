import contextlib

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
    # TODO: establish connection
    raise NotImplementedError
  else:
    raise NotImplementedError
