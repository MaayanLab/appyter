import re
from appyter.fields import Field

class TextListField(Field):
  ''' Representing a field that accepts a set of strings separated by newlines

  Be careful with this field, consider defining a constraint regex.
  ```eval_rst
  Unlike :class:`appyter.profiles.default.fields.TextField`, this class will return
   a list and potentially render differently.
  ```

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param choices: (Union[List[str], Set[str], Dict[str, str]]) A set of choices that are available for this field or lookup table mapping from choice label to resulting value
  :param constraint: (Regex[str]) A regular expression for validating the file name.
  :param default: (str) A default value as an example and for use during prototyping
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
    elif type(self.args['value']) == list:
      return self.args['value']
    elif self.args['value'] is None:
      return []
    else:
      return None

  @property
  def value(self):
    if type(self.choices) == dict:
      return [self.choices[v] for v in self.raw_value]
    else:
      assert self.constraint(), '%s[%s] (%s) does not satisfy constraints' % (
        self.field, self.args.get('name', ''), self.raw_value
      )
      return self.raw_value

  def constraint(self):
    return all([self.raw_value is not None] + [
      re.match(self.args['constraint'], val) is not None
      for val in self.raw_value
    ])
