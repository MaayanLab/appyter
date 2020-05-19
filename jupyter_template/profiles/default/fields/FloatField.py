from jupyter_template.fields import Field

class FloatField(Field):
  @property
  def raw_value(self):
    return float(self.args['value'])

  def constraint(self):
    return True
