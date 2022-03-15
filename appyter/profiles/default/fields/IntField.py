from appyter.fields import Field

class IntField(Field):
  ''' Representing a field that accepts an integer

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param min: (Optional[int]) the minimum valid value that the field can take on
  :param max: (Optional[int]) the maximum valid value that the field can take on
  :param step: (Optional[int]) the interval for which values are incremented or decremented
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (float) A default value as an example and for use during prototyping
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, min=None, max=None, step=None, **kwargs):
    super().__init__(
      min=min,
      max=max,
      step=step,
      **kwargs,
    )

  @property
  def raw_value(self):
    if self.args['value'] is None:
      return None
    else:
      return int(self.args['value'])

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      return (
        self.args['min'] is None or self.raw_value >= self.args['min']
      ) and (
        self.args['max'] is None or self.raw_value <= self.args['max']
      ) and (
        self.args['step'] is None or (self.raw_value - self.args.get('min', 0)) % self.args['step'] == 0
      )

  def to_jsonschema(self):
    schema = dict(super().to_jsonschema(), type='integer')
    if self.args.get('min') is not None: schema['minimum'] = self.args['min']
    if self.args.get('max') is not None: schema['maximum'] = self.args['max']
    return schema

  def to_cwl(self):
    return dict(super().to_cwl(), type='int')

  def to_click(self):
    args, kwargs = super().to_click()
    kwargs['type'] = int
    return args, kwargs
