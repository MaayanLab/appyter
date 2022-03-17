from appyter.execspec.registry import get_executor_class

def url_to_executor(url, **kwargs):
  proto, _, url = url.partition('::')
  cls = get_executor_class(proto)
  return cls(**cls.parse(url), **kwargs)
