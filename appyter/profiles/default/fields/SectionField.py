from appyter.fields import Field

class SectionField(Field):
  ''' Representing section header which other fields can be a part of
  ```python
  %%appyter hide_code
  {% do SectionField(name='section1', label='My Section') %}
  {% set x = IntField(name='int1', label='My Int', section='section1') %}
  ```
  '''

  def __init__(self, **kwargs):
    '''
    :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
    '''
    super().__init__(**kwargs)
    self['type'] = 'section'
