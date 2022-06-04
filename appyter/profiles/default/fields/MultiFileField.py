import re
from appyter.ext.itertools import ensure_list
from appyter.ext.re import re_full
from appyter.fields import Field, FieldConstraintException
from appyter.profiles.default.fields.FileField import FileField
from appyter.render.flask_app.upload import upload_from_request

class MultiFileField(FileField):
  def __init__(self, multiple=True, **kwargs):
    super().__init__(multiple=multiple, **kwargs)

  @property
  def raw_value(self):
    if type(self.args['value']) == str and self.args['value']:
      raw_value = self.args['value'].splitlines()
    elif type(self.args['value']) == list or type(self.args['value']) == tuple:
      raw_value = list(self.args['value'])
    else:
      raw_value = []
    return [v for v in raw_value if re.sub('\s+', '', v)]

  @property
  def uri(self):
    raise NotImplementedError

  @property
  def uris(self):
    return [
      self.prepare_uri(v)
      for v in self.raw_value
    ]

  def prepare(self, req):
    ''' Convert file in request into URI
    '''
    data_paths = None
    # get data from request upload
    if getattr(req, 'files', None):
      data_paths = upload_from_request(req, self.args['name'], multiple=True)
    # fallback to default (URI in request)
    if data_paths is None:
      data_paths = [s for f in ensure_list(Field.prepare(self, req)[self.args['name']]) for s in f.splitlines()]
    # convert strings into uris
    data_paths = [self.prepare_uri(data_path) for data_path in data_paths]
    data = {self.args['name']: [str(data_path) for data_path in data_paths]}
    for data_path in data_paths:
      if data_path.fragment_path:
        data.update({ f"_file:{data_path.fragment_path}": str(data_path.with_fragment_path(None))})
    return data

  def constraint(self):
    if not self.raw_value:
      return not self.args.get('required')
    else:
      expr = re.compile(re_full(self.args['constraint']))
      for uri in self.uris:
        if self._env.globals['_config']['SAFE_MODE']:
          if uri.scheme not in {'drs', 's3', 'gs', 'ftp', 'http', 'https', 'storage', 'user'}:
            return False
        if not expr.match(uri.fragment_path):
          return False
      return True

  @property
  def value(self):
    if not self.uris:
      return []
    if not self.constraint():
      raise FieldConstraintException(
        field=self.field,
        field_name=self.args['name'],
        value=self.raw_value,
      )
    return [uri.fragment_path for uri in self.uris]

  def to_cwl(self):
    schema = super().to_cwl()
    schema['inputBinding'].pop('prefix', None)
    if self.args.get('required') == True:
      schema['type'] = {
        'type': 'array',
        'items': 'File',
        'inputBinding': {
          'separate': False,
          'prefix': f"--{self.args['name']}="
        },
      }
    else:
      schema['type'] = [
        'null',
        {
          'type': 'array',
          'items': 'File',
          'inputBinding': {
            'separate': False,
            'prefix': f"--{self.args['name']}="
          },
        },
      ]
    return schema

  def to_cwl_value(self):
    return [
      {
        'class': 'File',
        'path': str(uri.with_fragment_path(None)),
        'name': uri.fragment_path,
      } for uri in self.uris
    ] if self.raw_value is not None else None

  def to_click(self):
    args, kwargs = super().to_click()
    kwargs['multiple'] = True
    return args, kwargs

  def to_jsonschema(self):
    schema = super().to_jsonschema()
    schema = {
      'type': 'array',
      'items': schema,
    }
    return schema

  @property
  def public_url(self):
    raise NotImplementedError

  @property
  def public_urls(self):
    return [
      str(uri.with_fragment_path(None))
      for uri in self.uris
    ]
