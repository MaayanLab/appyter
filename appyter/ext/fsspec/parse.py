from appyter.ext.urllib import parse_qs

def parse_file_uri_fragment(uri):
  if '#' in uri:
    uri, filename = uri.rsplit('#', 1)
  else:
    filename = uri.rstrip('/').rsplit('/')[-1]
  return uri, filename

def parse_file_uri_qs(uri):
  if '?' in uri:
    url, qs = uri.split('?', maxsplit=1)
    qs = parse_qs(qs)
  else:
    url = uri
    qs = {}
  return url, qs
