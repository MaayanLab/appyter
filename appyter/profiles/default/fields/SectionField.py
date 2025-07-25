from appyter.fields import Field

class SectionField(Field):
  r'''
  Representing section header which other fields can be a part of

  .. code-block:: python

    %%appyter hide_code
      {% do SectionField(name='section1', title='My Section', subtitle='is awesome') %}
      {% set x = IntField(name='int1', label='My Int', section='section1') %}

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param title: (str) A human readable title for the section
  :param subtitle: (str) A human readable subtitle for the section
  :param img: (str) The path to an image used in the field relative to the static folder
  :param icon: (str) A font-awesome icon identifier, used if img is not provided
  :param \**kwargs: Additional keyword arguments used by other fields
  '''
  def __init__(self, icon='cogs', **kwargs):
    super().__init__(icon=icon, **kwargs)
    self['type'] = 'section'

  @property
  def raw_value(self):
    raise Exception('DescriptionField has no value')

  def to_jsonschema(self):
    return None

  def to_cwl(self):
    return None

  def to_cwl_value(self):
    return None

  def to_click(self):
    return None
