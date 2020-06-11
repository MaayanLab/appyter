from appyter.fields import Field

class IntField(Field):
  ''' Representing a field that accepts an integer
  '''

  def __init__(self, min=0, max=10, **kwargs):
    '''
    :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
    :param label: (str) A human readable label for the field for the HTML form
    :param description: (Optional[str]) A long human readable description for the field for the HTML form
    :param min: (required) the minimum valid value that the field can take on
    :param max: (required) the maximum valid value that the field can take on
    :param default: (float) A default value as an example and for use during prototyping
    :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
    :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
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
