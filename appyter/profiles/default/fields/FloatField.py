from appyter.fields import Field

class FloatField(Field):
  ''' Representing a field that accepts a floating point value
  '''

  @property
  def raw_value(self):
    return float(self.args['value'])

  def constraint(self):
    # Raw value would fail otherwise
    return True
