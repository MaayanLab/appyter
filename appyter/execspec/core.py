import re
from appyter.execspec.registry import get_executor_class

def url_to_executor(url, **kwargs):
  m = re.match(r"^([^:#?]+)(::|://)?(.*)$", url)
  assert m is not None, "Invalid executor spec"
  proto = m.group(1)
  if m.group(2) == '::':
    url = m.group(3)
  else:
    url = m.group(0)
  cls = get_executor_class(proto)
  return cls(**cls.parse(url), **kwargs)
