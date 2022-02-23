
def sanitize_sha1sum(val):
  import re
  m = re.match(r'^[0-9a-f]{40}$', val)
  return val if m else None

def generate_uuid():
  import uuid
  return str(uuid.uuid4())

def sanitize_uuid(val):
  import uuid
  try:
    return str(uuid.UUID(val))
  except ValueError:
    return None
