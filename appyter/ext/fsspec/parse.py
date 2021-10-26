
def parse_file_uri(uri):
  if '#' in uri:
    uri, filename = uri.rsplit('#', 1)
  else:
    filename = uri.rstrip('/').rsplit('/')[-1]
  return uri, filename