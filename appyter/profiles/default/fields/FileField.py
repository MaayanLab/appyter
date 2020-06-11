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
    :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
    :param label: (str) A human readable label for the field for the HTML form
    :param description: (Optional[str]) A long human readable description for the field for the HTML form
    :param constraint: A regular expression for validating the file name.
    :param default: (Any) A default value as an example and for use during prototyping
    :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
    :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
    :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
    '''
    super(FileField, self).__init__(
      constraint=constraint,
      **kwargs,
    )

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)
