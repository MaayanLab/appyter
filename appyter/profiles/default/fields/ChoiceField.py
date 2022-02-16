from appyter.fields import Field

class ChoiceField(Field):
  ''' Represing a choice of string values with a combo box.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param choices: (Union[List[str], Dict[str, str]]) A set of choices that are available for this field or lookup table mapping from choice label to resulting value
  :param default: (str) A default value as an example and for use during prototyping
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    assert self.choices, 'ChoiceField requires choices'

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      return self.raw_value in self.choices

  @property
  def safe_value(self):
    return self.value
