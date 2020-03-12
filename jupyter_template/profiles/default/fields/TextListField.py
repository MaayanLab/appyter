import re
from jupyter_template.fields import Field

class TextListField(Field):
  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    super(TextListField, self).__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)

  @property
  def raw_value(self):
    return self.args['value'].split('\n')
