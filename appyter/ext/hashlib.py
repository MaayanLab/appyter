import functools

def hashsum_io(algo, io, chunk_size=65536):
  import hashlib
  hashsum = hashlib.new(algo)
  while True:
    buf = io.read(chunk_size)
    if not buf: break
    hashsum.update(buf)
  return hashsum.hexdigest()

sha1sum_io = functools.partial(hashsum_io, 'sha1')

def hashsum_dict(algo, obj):
  import json, hashlib
  sha1 = hashlib.new(algo)
  sha1.update(json.dumps(obj, sort_keys=True, separators=None, ensure_ascii=True).encode())
  return sha1.hexdigest()

sha1sum_dict = functools.partial(hashsum_dict, 'sha1')