from appyter.fields import Field

class DescriptionField(Field):
  ''' Representing text between fields

  Usage:
  ```python
  {% do DescriptionField(
    name='my_fieldname',
    text='My Description',
  ) %}
  ```

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param text: (str) A human readable, HTML parsable text
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)

  def value(self):
    raise Exception('DescriptionField cannot be rendered')
