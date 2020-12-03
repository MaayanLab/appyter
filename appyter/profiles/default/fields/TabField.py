import logging
logger = logging.getLogger(__name__)

from appyter.fields import Field
from appyter.util import collapse, try_json_loads

class TabField(Field):
  '''
  Usage:
    ```j2
    {{ TabField(
      choices={
        "A": [
          StringField(
            name="A",
            default="a"
          ),
        ],
        "B": [
          StringField(
            name="B",
            default="b"
          )
        ]
      }
    ) }}
    ```
  '''
  def __init__(self, choices={}, **kwargs):
    super(TabField, self).__init__(choices=choices, **kwargs)

  def prepare(self, req):
    logger.debug(f"prepare")
    data = {}
    if type(req) == dict:
      data[self.args['name']] = self.args['value'] = req.get(self.args['name'])
    elif req.json:
      data[self.args['name']] = self.args['value'] = req.json.get(self.args['name'])
    elif req.form:
      data[self.args['name']] = self.args['value'] = collapse(req.form.getlist(self.args['name']))
    else:
      raise NotImplementedError
    data.update(self.value.prepare(req))
    return data

  def pre_construct(self, ctx, **kwargs):
    logger.debug(f"pre_construct")
    self.args['value'] = ctx.get(self.args['name'])
    return self.value.pre_construct(ctx, **kwargs)

  def post_construct(self, ctx, **kwargs):
    logger.debug(f"post_construct")
    self.args['value'] = ctx.get(self.args['name'])
    return self.value.post_construct(ctx, **kwargs)

  def constraint(self):
    return self.raw_value is not None and all(v in self.choices for v in self.raw_value)

  def render(self, **kwargs):
    self.args['field_renders'] = {
      field.args['name']: str(field.render())
      for tab_fields in self.args['choices'].values()
      for field in tab_fields
    }
    return super().render(**kwargs)
