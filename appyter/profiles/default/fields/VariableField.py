import re
from appyter.fields import Field
from appyter.util import secure_filepath, join_routes

class VariableField(Field):
  ''' Represing a variable number of instances of a given Field
  Usage:
  ```j2
  {{ VariableField(
    field=FileField(
      name='file_field_name',
      default='file.txt',
    ),
    default=1,
    min=0,
    max=10,
  ) }}
  ```

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param default: (list) A default value as an example and for use during prototyping
  :param min: (int) The minimum number of fields that can be specified
  :param max: (int) The maximum number of fields that can be specified
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, field=None, **kwargs):
    assert isinstance(field, Field)
    super().__init__(
      field=field,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and all(self.args['field'](value=v).constraint() for v in self.raw_value)

  def render(self, **kwargs):
    self.args['field_render'] = str(self.args['field'].render())
    return super().render(**kwargs)
