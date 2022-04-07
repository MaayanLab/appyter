import re
from appyter.fields import Field
from appyter.ext.re import re_full

class URIFileField(Field):
  ''' Representing a field that accepts a file URI

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (str) A default value as an example and for use during prototyping
  :param examples: (Optional[Union[List[str], Dict[str, str]]]) Named strings to provide as clickable examples
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, description='One of several supported identifiers for accessing your file', required=None, **kwargs):
    super().__init__(
      description=description,
      constraint='^(drs|s3|gs|ftp|http|https)://.+$',
      hint='e.g. drs://yourhost.com/yourid...',
      feedback='Supported protocols include: drs (GA4GH), s3, gs, ftp, http, & https',
      required=required,
      **kwargs,
    )

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      return re.match(re_full(self.args['constraint']), self.raw_value)

  def to_jsonschema(self):
    schema = super().to_jsonschema()
    if self.args.get('constraint'): schema['pattern'] = re_full(self.args['constraint'])
    return schema
