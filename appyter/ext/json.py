import json

def try_json_loads(v):
  try:
    return json.loads(v)
  except TypeError:
    return v
  except json.JSONDecodeError:
    return v

def try_json_dumps(v):
  if type(v) == str:
    return v
  else:
    return json.dumps(v)

from appyter.ext.asyncio.helpers import ensure_async
async_json_loads = ensure_async(json.loads)
async_json_dumps = ensure_async(json.dumps)
