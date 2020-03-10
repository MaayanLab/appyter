from jupyter_template.fields import register, Field

@register
class IntField(Field):
  def __init__(self, min=0, max=10, **kwargs):
    super(IntField, self).__init__(
      min=min,
      max=max,
      **kwargs,
    )

  @property
  def raw_value(self):
    return int(self.args['value'])

  @property
  def choices(self):
    return list(range(self.args['min'], self.args['max']))

  def constraint(self):
    return self.raw_value >= self.args['min'] and self.raw_value <= self.args['max']
