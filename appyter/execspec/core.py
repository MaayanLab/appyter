from appyter.execspec.registry import get_executor_class

def url_to_executor(url, **kwargs):
  if '::' in url:
    proto, _, url = url.partition('::')
  elif '?' in url:
    proto, *conf = url.partition('?')
    url = ''.join(conf)
  cls = get_executor_class(proto)
  return cls(**cls.parse(url), **kwargs)
