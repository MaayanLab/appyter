from appyter.fields import Field
from appyter.ext.dict import dict_collision_free_update

class TabField(Field):
  ''' Representing a tab field which contains inner fields to choose from.
  ```python
  %%appyter hide_code
  {% myfield = TabField(
    name='my_field',
    choices={
      "A": [
        StringField(
          name="my_field_A",
          default="a"
        ),
      ],
      "B": [
        StringField(
          name="my_field_B",
          default="b"
        )
      ]
    }
  ) %}

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param \**kwargs: Additional keyword arguments used by other fields
  ```
  '''
  def __init__(self, choices={}, **kwargs):
    super(TabField, self).__init__(choices=choices, **kwargs)
    assert self.choices and type(self.choices) == dict, 'TabField requires choices'
    for section, fields in self.choices.items():
      for field in fields:
        field['args']['parent'] = self.args['name']
    if not self.args.get('default'):
      self.args['default'] = next(iter(self.choices))

  def prepare(self, req):
    data = super().prepare(req)
    for value in self.value:
      dict_collision_free_update(data, **value.prepare(req))
    return data

  def constraint(self):
    if not self.raw_value:
      return not self.args.get('required')
    else:
      return all(v in self.choices for v in self.raw_value)
