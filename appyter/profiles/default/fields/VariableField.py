from appyter.fields import Field
from appyter.util import collapse, ensure_list, try_json_loads, resolve_json_ref

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
      examples={},
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
    data = {}
    if getattr(req, 'form', None):
      data[self.args['name']] = self.args['value'] = collapse([
        resolve_json_ref(v, lambda k: try_json_loads(collapse(req.form.getlist(k))))
        for v in ensure_list(try_json_loads(collapse(req.form.getlist(self.args['name']))))
      ])
    else:
      data.update(super().prepare(req))
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
