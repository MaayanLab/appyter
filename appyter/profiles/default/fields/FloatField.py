from appyter.fields import Field

class FloatField(Field):
  ''' Representing a field that accepts a floating point value

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (float) A default value as an example and for use during prototyping
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  @property
  def raw_value(self):
    if self.args['value'] is None:
      return None
    else:
      return float(self.args['value'])

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      # Raw value would fail otherwise
      return True

  def to_jsonschema(self):
    return dict(super().to_jsonschema(), type='numeric')

  def to_cwl(self):
    return dict(super().to_cwl(), type='float')

  def to_click(self):
    args, kwargs = super().to_click()
    kwargs['type'] = float
    return args, kwargs
