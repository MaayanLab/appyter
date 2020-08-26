import json

def jsonify_repr(v):
  if type(v) == str:
    return json.dumps(v)
  elif type(v) == list:
    return json.dumps(','.join(map(str, v)))
  else:
    return json.dumps(json.dumps(v))
