
def dict_filter_none(d):
  return { k: v for k, v in d.items() if v }

def dict_collision_free_update(d, **kwargs):
  for k, v in kwargs.items():
    assert k not in d, 'Collision in update'
    d[k] = v
