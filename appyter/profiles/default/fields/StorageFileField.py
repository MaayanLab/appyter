from appyter.profiles.default.fields.FileField import FileField

class StorageFileField(FileField):
  ''' Represing a File selectable from background storage
  The field ends up being a string of the file path, for example:
  ```python
  import pandas as pd
  df = pd.read_csv({{ StorageFileField(name='my-csv', label='My CSV', storage='storage://') }})
  ```

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param constraint: A regular expression for validating the file name.
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (str) A default value as an example and for use during prototyping
  :param storage: (str) The storage backend to select the file from
  :param examples: (Optional[Dict[str, str]]) Named url paths to example files to upload
    paths can be relative i.e. `{ "my_file.txt": url_for('static', filename='my_file.txt') }`, or a remote url.
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, constraint=r'.*', examples={}, **kwargs):
    super().__init__(
      constraint=constraint,
      examples=examples,
      **kwargs,
    )

  @property
  def public_url(self):
    return self.args['storage'] + self.raw_value
