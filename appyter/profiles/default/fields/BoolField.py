import json
from appyter.fields import Field

class BoolField(Field):
  ''' Represing a true or false value with a checkbox.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (bool) A default value as an example and for use during prototyping
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  @property
  def raw_value(self):
    if self.args['value'] in {'on', 'checked', 'yes', 'true', 'True', True}:
      return True
    elif self.args['value'] in {'off', 'unchecked', 'no', 'false', 'False', False}:
      return False
    elif self.args['value'] is None and not self.args.get('required'):
      return None
    else:
      raise Exception('Invalid value for bool field')

  @property
  def choices(self):
    return [True, False]
