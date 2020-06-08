import re
from appyter.fields import Field

class TextListField(Field):
  ''' Representing a field that accepts a set of strings separated by newlines

  Be careful with this field, consider defining a constraint regex.
  ```eval_rst
  Unlike :class:`appyter.profiles.default.fields.TextField`, this class will return
   a list and potentially render differently.
  ```
  '''

  def __init__(self, constraint=r'[^\n]*', hint=None, **kwargs):
    '''
    :param constraint: A regular expression for validating the file name.
    :param hint: A hint to put in the field prior to content.
    :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
    '''
    super(TextListField, self).__init__(
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
