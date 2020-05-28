from appyter.fields import Field

class ChoiceField(Field):
  def constraint(self):
    return self.raw_value is not None and self.raw_value in self.choices

  @property
  def safe_value(self):
    return self.value
