
def sha1sum_io(io, chunk_size=65536):
  import hashlib
  sha1 = hashlib.sha1()
  while True:
    buf = io.read(chunk_size)
    if not buf: break
    sha1.update(buf)
  return sha1.hexdigest()

def sha1sum_dict(obj):
  import json, hashlib
  sha1 = hashlib.sha1()
  sha1.update(json.dumps(obj, sort_keys=True, separators=None, ensure_ascii=True).encode())
  return sha1.hexdigest()
