import re
from jupyter_template.fields import Field

class FileField(Field):
  def __init__(self, constraint=r'[^/]*', **kwargs):
    super(FileField, self).__init__(
      constraint=constraint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)
