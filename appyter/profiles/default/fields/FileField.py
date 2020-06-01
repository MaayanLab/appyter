import re
from appyter.fields import Field

class FileField(Field):
  ''' Represing a uploadable File and facilitating that file upload.
  The field ends up being a string of the file path, for example:
  ```python
  import pandas as pd
  df = pd.read_csv({{ FileField(name='my-csv', label='My CSV') }})
  ```
  '''

  def __init__(self, constraint=r'[^/]*', **kwargs):
    '''
    :param constraint: A regular expression for validating the file name.
    :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
    '''
    super(FileField, self).__init__(
      constraint=constraint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)
