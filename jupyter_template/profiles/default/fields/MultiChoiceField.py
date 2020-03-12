from jupyter_template.fields import Field

class MultiChoiceField(Field):
  @property
  def raw_value(self):
    if type(self.args['value']) == str:
      return [self.args['value']]
    elif type(self.args['value']) == list:
      return self.args['value']
    elif self.args['value'] is None:
      return []
    else:
      return None

  def constraint(self):
    return self.raw_value is not None and all(v in self.choices for v in self.raw_value)
