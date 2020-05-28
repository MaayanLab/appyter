from appyter.fields import Field

class SectionField(Field):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self['type'] = 'section'