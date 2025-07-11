from appyter.fields import Field, FieldConstraintException
from appyter.ext.json import try_json_loads

class MultiChoiceField(Field):
  r''' Represing a multi-selectable combo box.
  The resulting selection is represented with a list of strings that were chosen.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param choices: (Union[List[str], Dict[str, str]]) A set of choices that are available for this field or lookup table mapping from choice label to resulting value
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (float) A default value as an example and for use during prototyping
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    assert self.choices, 'MultiChoiceField requires choices'

  @property
  def raw_value(self):
    value = try_json_loads(self.args['value'])
    if not value:
      return []
    elif type(value) == list:
      return value
    elif type(value) == str:
      return [value]
    else:
      return [self.args['value']]

  def constraint(self):
    if not self.raw_value:
      return not self.args.get('required')
    else:
      return type(self.raw_value) == list and all(v in self.choices for v in self.raw_value)

  @property
  def value(self):
    if not self.constraint():
      raise FieldConstraintException(
        field=self.field,
        field_name=self.args['name'],
        value=self.raw_value,
      )
    elif type(self.choices) == dict:
      return [self.choices[v] for v in self.raw_value]
    else:
      return self.raw_value

  def to_jsonschema(self):
    schema = {'type': 'array', 'items': { 'type': 'string' } }
    if self.args.get('label'): schema['title'] = self.args['label']
    if self.args.get('description'): schema['description'] = self.args['description']
    if self.args.get('choices'): schema['items']['enum'] = list(self.args['choices'])
    if self.args.get('default'): schema['default'] = self.args['default']
    return schema

  def to_cwl(self):
    schema = super().to_cwl()
    # NOTE: CWL's array enum is broken upstream
    # if self.args.get('required') == True:
    #   schema['type'] = {
    #     'type': 'array',
    #     'items': {
    #       'type': 'enum',
    #       'symbols': list(self.args['choices'])
    #     },
    #   }
    # else:
    #   schema['type'] = ['null', {
    #     'type': 'array',
    #     'items': {
    #       'type': 'enum',
    #       'symbols': list(self.args['choices'])
    #     },
    #   }]
    schema['type'] = f"string{'' if self.args.get('required') == True else '?'}"
    return schema

  def to_cwl_value(self):
    import json
    return json.dumps(self.raw_value)

  def to_click(self):
    args, kwargs = super().to_click()
    # kwargs['multiple'] = True
    import click
    kwargs['type'] = click.STRING
    return args, kwargs
