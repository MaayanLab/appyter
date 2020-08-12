from appyter.fields import Field

class DescriptionField(Field):
  ''' Representing text between fields

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param text: (str) A human readable, HTML parsable text
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
