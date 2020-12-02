import re
from appyter.fields import Field
from appyter.util import secure_filepath, join_routes
from appyter.util import try_json_loads

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

  @property
  def raw_value(self):
    value = try_json_loads(self.args['value'])
    if value is None:
      return []
    elif type(value) == list:
      return value
    elif type(value) == str:
      return [value]
    else:
      return [self.args['value']]

  def constraint(self):
    return self.args['min'] <= len(self.raw_value) <= self.args['max'] and all(
      v.startswith(self.args['field']['args']['name'])
      for v in self.raw_value
    )

  @property
  def value(self):
    assert self.constraint(), '%s[%s] (%s) does not satisfy constraints' % (
      self.field, self.args.get('name', ''), self.raw_value
    )
    # TODO: grab fields from environment
    return [
      self._env.globals[name]
      for name in self.raw_value
    ]

  def render(self, **kwargs):
    self.args['field']['js_url'] = self.args['field'].js_url
    return super().render(**kwargs)
