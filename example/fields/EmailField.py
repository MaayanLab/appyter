from jupyter_template.fields import Field

class EmailField(Field):
  def __init__(self, **kwargs):
    super(EmailField, self).__init__(**kwargs)

  def template(self):
    import os
    return os.path.join(os.path.dirname(__file__), 'EmailField.j2')

  def constraint(self):
    import re
    return self.raw_value is not None and re.match(r'\w[\w\d_-]+@\w[\w\d_-]+\.\w[\w\d_-]+', self.raw_value)
