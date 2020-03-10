import re
from jupyter_template.fields import register, Field

@register
class TextField(Field):
  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    super(TextField, self).__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)
