import re
from appyter.fields import Field

class TextField(Field):
  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    super(TextField, self).__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)

  @property
  def safe_value(self):
    # use repr to escape things, revert newlines
    v = repr(self.value).replace('\\r', '\r').replace('\\n', '\n')
    # convert single to triple quotes
    return v[0] + v[0] + v + v[0] + v[0]
