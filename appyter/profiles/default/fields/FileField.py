import re
from appyter.fields import Field, FieldConstraintException
from appyter.render.flask_app.upload import upload_from_request
from appyter.ext.flask import secure_filepath
from appyter.ext.urllib import URI
from appyter.ext.re import re_full

class FileField(Field):
  ''' Representing a File URL.

  The field ends up being a string of the file path, which will be relative to the appyter notebook.
  ```python
  import pandas as pd
  df = pd.read_csv({{ FileField(name='my-csv', label='My CSV') }})
  ```

  Importantly, a FileField ultimately resolves to a URL supporting several schemes. Appyters ensure
   that url is available as an actual file when the appyter executes.

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param constraint: A regular expression for validating the file name.
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (str) A default value as an example and for use during prototyping
  :param storage: (Optional[str]) A storage prefix for browsing
  :param examples: (Optional[Dict[str, str]]) Named url paths to example files to upload
    paths can be relative i.e. `{ "my_file.txt": url_for('static', filename='my_file.txt') }`, or a remote url.
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, default=None, constraint=r'.*', **kwargs):
    super().__init__(
      constraint=constraint,
      default=default,
      **kwargs,
    )

  @property
  def raw_value(self):
    if type(self.args['value']) == str and self.args['value']:
      return self.args['value']
    else:
      return None

  def prepare_uri(self, raw_value):
    ''' The fully resolved URI for this file
    '''
    if raw_value is None: return None
    uri_parsed = URI(raw_value)
    if uri_parsed.scheme is None:
      if self._env.globals['_config']['SAFE_MODE']:
        uri_parsed = (
          URI(self._env.globals['_config']['PUBLIC_URL'])
            .join('static', uri_parsed.path)
            .with_query_string(uri_parsed.query_string)
            .with_fragment_path(secure_filepath(uri_parsed.fragment_name or uri_parsed.name))
            .with_fragment_query_string(uri_parsed.fragment_query_string)
        )
      else:
        uri_parsed = uri_parsed.with_scheme('file').with_fragment_path(raw_value)
    if uri_parsed.fragment_path is None:
      uri_parsed = uri_parsed.with_fragment_path(uri_parsed.name)
    return uri_parsed

  @property
  def uri(self):
    return self.prepare_uri(self.raw_value)

  def prepare(self, req):
    ''' Convert file in request into URI
    '''
    data_path = None
    # get data from request upload
    if getattr(req, 'files', None):
      data_path = upload_from_request(req, self.args['name'])
    # fallback to default (URI in request)
    if data_path is None: data_path = super().prepare(req)[self.args['name']]
    data_path = self.prepare_uri(data_path)
    data = {self.args['name']: str(data_path)}
    if data_path.fragment_path:
      data.update({ f"_file:{data_path.fragment_path}": str(data_path.with_fragment_path(None))})
    return data

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      if self._env.globals['_config']['SAFE_MODE']:
        if self.uri.scheme not in {'drs', 's3', 'gs', 'ftp', 'http', 'https', 'storage', 'user'}:
          return False
      return re.match(re_full(self.args['constraint']), self.uri.fragment_path)

  @property
  def value(self):
    if self.uri is None:
      return None
    if not self.constraint():
      raise FieldConstraintException(
        field=self.field,
        field_name=self.args['name'],
        value=self.raw_value,
      )
    return self.uri.fragment_path

  def to_cwl(self):
    schema = super().to_cwl()
    schema['type'] = f"File{'' if self.args.get('required') == True else '?'}"
    return schema

  def to_cwl_value(self):
    return {
      'class': 'File',
      'path': str(self.uri.with_fragment_path(None)),
      'name': self.uri.fragment_path,
    } if self.raw_value is not None else None

  def to_jsonschema(self):
    schema = super().to_jsonschema()
    if self.args.get('constraint'): schema['pattern'] = re_full(self.args['constraint'])
    return schema

  @property
  def public_url(self):
    return str(self.uri.with_fragment_path(None))
