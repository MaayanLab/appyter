import json
from jupyter_template.fields import register, Field

@register
class BoolField(Field):
  @property
  def raw_value(self):
    return self.args['value'] if type(self.args['value']) == bool else bool(json.loads(self.args['value'].lower()))

  @property
  def choices(self):
    return [True, False]
