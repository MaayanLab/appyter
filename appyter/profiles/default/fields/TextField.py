import re
from appyter.fields import Field
from appyter.util import re_full

class TextField(Field):
  ''' Representing a field that accepts a multi-line string

  Be careful with this field, consider defining a constraint regex.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param constraint: (Regex[str]) A regular expression for validating the file name.
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (str) A default value as an example and for use during prototyping
  :param examples: (Optional[Dict[str, str]]) Named strings to provide as clickable examples
  :param hint: (Optional[str]) A hint to put in the field prior to content.
  :param rows: (Optional[int]) The number of rows (lines) in the textarea
  :param cols: (Optional[int]) The number of cols (horizontal characters) in the textarea
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    super().__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      return re.match(re_full(self.args['constraint']), self.raw_value, re.MULTILINE | re.DOTALL)

  @property
  def safe_value(self):
    # use repr to escape things, revert newlines
    v = repr(self.value).replace('\\r', '\r').replace('\\n', '\n')
    # convert single to triple quotes
    return v[0] + v[0] + v + v[0] + v[0]
