import re
from appyter.fields import Field, FieldConstraintException
from appyter.ext.re import re_full

class TextListField(Field):
  r''' Representing a field that accepts a set of strings separated by newlines

  Be careful with this field, consider defining a constraint regex.
  
  Unlike :class:`appyter.profiles.default.fields.TextField`, this class will return
  a list and potentially render differently.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param choices: (Union[List[str], Dict[str, str]]) A set of choices that are available for this field or lookup table mapping from choice label to resulting value
  :param constraint: (Regex[str]) A regular expression for validating the file name.
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (List[str]) A default value as an example and for use during prototyping
  :param examples: (Optional[Dict[str, List[str]]]) Named lists to provide as clickable examples
  :param hint: (Optional[str]) A hint to put in the field prior to content.
  :param rows: (Optional[int]) The number of rows (lines) in the textarea
  :param cols: (Optional[int]) The number of cols (horizontal characters) in the textarea
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, constraint=r'[^\n]*', hint=None, **kwargs):
    super().__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  @property
  def raw_value(self):
    if type(self.args['value']) == str:
      return list(
        filter(None,
          map(str.strip,
            self.args['value'].splitlines()
          )
        )
      )
    elif type(self.args['value']) == list or type(self.args['value']) == tuple:
      return list(self.args['value'])
    elif self.args['value'] is None:
      return []
    else:
      return None

  def constraint(self):
    if not self.raw_value:
      return not self.args.get('required')
    else:
      return all([
        re.match(re_full(self.args['constraint']), val)
        for val in self.raw_value
      ])

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
    if self.args.get('constraint'): schema['items']['pattern'] = re_full(self.args['constraint'])
    if self.args.get('default'): schema['default'] = self.args['default']
    return schema

  def to_cwl(self):
    schema = super().to_cwl()
    # NOTE: CWL's array enum is broken upstream
    # if self.args.get('choices'):
    #   if self.args.get('required') == True:
    #     schema['type'] = {
    #       'type': 'array',
    #       'items': {
    #         'type': 'enum',
    #         'symbols': list(self.args['choices'])
    #       },
    #     }
    #   else:
    #     schema['type'] = ['null', {
    #       'type': 'array',
    #       'items': {
    #         'type': 'enum',
    #         'symbols': list(self.args['choices'])
    #       },
    #     }]
    schema['type'] = f"string{'' if self.args.get('required') == True else '?'}"
    return schema

  def to_cwl_value(self):
    return '\n'.join(self.raw_value)

  def to_click(self):
    args, kwargs = super().to_click()
    # kwargs['multiple'] = True
    import click
    kwargs['type'] = click.STRING
    return args, kwargs
