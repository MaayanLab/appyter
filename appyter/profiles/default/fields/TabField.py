from appyter.fields import Field

class TabField(Field):
  '''
  Usage:
    ```j2
    {{ TabField(
      choices={
        "A": [
          StringField(
            name="A",
            default="a"
          ),
        ],
        "B": [
          StringField(
            name="B",
            default="b"
          )
        ]
      }
    ) }}
    ```
  '''
  def __init__(self, choices={}, **kwargs):
    super(TabField, self).__init__(choices=choices, **kwargs)

  def constraint(self):
    return self.raw_value is not None and all(v in self.choices for v in self.raw_value)

  def render(self, **kwargs):
    self.args['field_renders'] = {
      field.args['name']: str(field.render())
      for tab_fields in self.args['choices'].values()
      for field in tab_fields
    }
    return super().render(**kwargs)
