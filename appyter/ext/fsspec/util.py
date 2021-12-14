def split_protocol_opts(url, default_protocol='file'):
  ''' Like `fsspec.core.split_protocol`
  but remove fragments potentially parsing querystrings in the fragment as filesystem opts

  url of the form: proto://netloc/path?qs=anything#ignored?protocol.options=here
  '''
  from appyter.ext.urllib import parse_file_uri
  from fsspec.core import url_to_fs, split_protocol
  uri_parsed = parse_file_uri(url)
  opts = uri_parsed.fragment_qs or {}
  uri_parsed.fragment = None
  uri_parsed.fragment_query = None
  protocol, path = split_protocol(str(uri_parsed))
  protocol = protocol or default_protocol
  return protocol, path, opts
