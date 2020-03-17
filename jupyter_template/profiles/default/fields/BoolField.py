import json
from jupyter_template.fields import Field

class BoolField(Field):
  @property
  def raw_value(self):
    if self.args['value'] in {'on', 'checked', 'yes', 'true', 'True', True}:
      return True
    elif self.args['value'] in {'off', 'unchecked', 'no', 'false', 'False', False}:
      return False
    else:
      raise Exception('Invalid value for bool field')

  @property
  def choices(self):
    return [True, False]
