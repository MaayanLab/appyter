import re
from jupyter_template.fields import Field

class StringField(Field):
  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    super(StringField, self).__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)
