import re
from appyter.fields import Field

class StringField(Field):
  ''' Representing a field that accepts a string

  Be careful with this field, consider defining a constraint regex.
  '''

  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    '''
    :param constraint: A regular expression for validating the file name.
    :param hint: A hint to put in the field prior to content.
    :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
    '''
    super(StringField, self).__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)
