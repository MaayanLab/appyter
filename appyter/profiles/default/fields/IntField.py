from appyter.fields import Field

class IntField(Field):
  ''' Representing a field that accepts an integer
  '''

  def __init__(self, min=0, max=10, **kwargs):
    '''
    :param min: (required) the minimum valid value that the field can take on
    :param max: (required) the maximum valid value that the field can take on
    :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
    '''
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
