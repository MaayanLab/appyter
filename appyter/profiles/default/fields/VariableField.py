import re
from appyter.fields import Field
from appyter.ext.json import try_json_loads
from appyter.ext.itertools import ensure_list

class VariableField(Field):
  ''' Represing a variable number of instances of a given Field
  Usage:
  ```j2
  {{ VariableField(
    nane='files'
    label='Files',
    field=FileField(
      name='file',
      label='File',
      default='file.txt',
    ),
    default=['file.txt'],
    min=0,
    max=10,
  ) }}
  ```
  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param default: (list) A default value as an example and for use during prototyping
  :param min: (int) The minimum number of fields that can be specified
  :param max: (int) The maximum number of fields that can be specified
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, field=None, **kwargs):
    super().__init__(
      field=field,
      **kwargs,
    )
    field['args']['parent'] = self.args['name']
  #
  def prepare(self, req):
    ''' Typically, you'll just provide a list of values satisfying the Field type,
    for forms we support json pointer refs for compatibility with older form fields -- these
    pointers are resolved during prepare. Basically:

    ```json
    {
      "variablefield": [{"$ref":"#/singlefield0"},{"$ref":"#/singlefield1"}],
      "singlefield0": "a",
      "singlefield1": "b"
    }
    ```json
    Will resolve to
    ```json
    {"variablefield": ["a", "b"]}
    ```

    Letting us construct the form as before but permitting us to reference form fields
     generated on the fly that end up in the form request.
    '''
    data = super().prepare(req)
    expr = re.compile(r'^#/([^/]+)$')
    value = []
    for i, v in enumerate(ensure_list(try_json_loads(data[self.args['name']]))):
      # resolve json pointers
      if type(v) == dict and len(v) == 1 and '$ref' in v:
        ptr = v['$ref']
        m = expr.match(ptr)
        if m:
          name = m.group(1)
          # prepare from pointer to value in request
          data.update(
            self._env.globals[self.args['field']['field']](
              name=name,
            ).prepare(req)
          )
          value.append(data.pop(name))
          continue
      # prepare with value provided using field
      name = f"{self.args['field']['args']['name']}{i}"
      data.update(
        self._env.globals[self.args['field']['field']](
          name=name,
        ).prepare({name: v})
      )
      value.append(data.pop(name))
    # return prepared aggregated value
    self.args['value'] = value
    data[self.args['name']] = value
    return data
  #
  @property
  def raw_value(self):
    value = try_json_loads(self.args['value'])
    if value is None:
      return []
    elif type(value) == list:
      return value
    else:
      return [self.args['value']]
  #
  def constraint(self):
    ''' Number of values should satisfy bounded constraints and
    all values should satisfy the field constraints.
    '''
    return self.args['min'] <= len(self.raw_value) <= self.args['max'] and all(
      self._env.globals[self.args['field']['field']](
        name=self.args['field']['args']['name'],
        value=v
      ).constraint()
      for v in self.raw_value
    )
  #
  @property
  def value(self):
    return [
      self._env.globals[self.args['field']['field']](
        name=self.args['field']['args']['name'],
        value=v
      ).value
      for v in self.raw_value
    ]
