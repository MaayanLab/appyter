import json

def jsonify_repr(v):
  return json.dumps(v) if type(v) == str else json.dumps(json.dumps(v))
