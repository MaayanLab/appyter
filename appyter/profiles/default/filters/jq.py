import json
from jq import jq as JQ

def jq(obj, id_query, query):
  obj_lookup = dict(zip(JQ(id_query).transform(obj, multiple_output=True), obj))
  results = JQ(query).transform(obj, multiple_output=True)
  result_ids = JQ(id_query).transform(results, multiple_output=True)
  return [obj_lookup[id] for id, result in zip(result_ids, results)]
