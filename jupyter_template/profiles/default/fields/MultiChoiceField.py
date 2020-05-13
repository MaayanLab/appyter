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

  @property
  def value(self):
    if type(self.choices) == dict:
      return [self.choices[v] for v in self.raw_value]
    else:
      assert self.constraint(), '%s[%s] (%s) does not satisfy constraints' % (
        self.field, self.args.get('name', ''), self.raw_value
      )
      return self.raw_value

  def constraint(self):
    return self.raw_value is not None and all(v in self.choices for v in self.raw_value)
