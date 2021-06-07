import re
from appyter.fields import Field
from appyter.util import re_full

class AutocompleteField(Field):
  ''' Representing a field that accepts a string with autocomplete.
  Auto complete will use `choices` or alternatively `file_path` -- a url to load the choices as an array.

  Be careful with this field, consider defining a constraint regex. Note that it is equivalent to
   a string field, and still accepts choices not being autocompleted.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param constraint: A regular expression for validating the file name.
  :param hint: A hint to put in the field prior to content.
  :param file_path: (Optional[str]) A remote url to download the autocomplete list. Should resolve to a json list of terms.
  :param choices: (Union[List[str], Set[str], Dict[str, str]]) A set of choices that are available for this field or lookup table mapping from choice label to resulting value
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (str) A default value as an example and for use during prototyping
  :param examples: (Optional[Dict[str, str]]) Named strings to provide as clickable examples
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, constraint=r'.*', hint=None, **kwargs):
    super().__init__(
      constraint=constraint,
      hint=hint,
      **kwargs,
    )
    assert bool(self.choices) ^ bool(self.args.get('file_path')), 'AutocompleteField requires choices or file_path but not both'

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    elif self.choices:
      return self.raw_value in self.choices
    else:
      return re.match(re_full(self.args['constraint']), self.raw_value)
