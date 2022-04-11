import re
from appyter.fields import Field, FieldConstraintException
from appyter.render.flask_app.upload import upload_from_request
from appyter.ext.flask import join_routes, secure_filepath
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
    if default and '://' not in default:
      default = f"storage://static/{default}"
    super().__init__(
      constraint=constraint,
      default=default,
      **kwargs,
    )

  @property
  def raw_value(self):
    if type(self.args['value']) == str and self.args['value']:
      uri_parsed = URI(self.args['value'])
      if self._env.globals['_config']['SAFE_MODE']:
        if uri_parsed.scheme not in {'drs', 's3', 'gs', 'ftp', 'http', 'https', 'storage'}:
          raise FieldConstraintException(self.field, self.args['name'], self.args['value'], message='Scheme not supported')
        return secure_filepath(uri_parsed.fragment_path or uri_parsed.name or self.args['value'])
      else:
        return uri_parsed.fragment_path or self.args['value']
    else:
      return None

  def prepare(self, req):
    ''' Convert file in request into URI
    '''
    if getattr(req, 'files', None):
      data_path = upload_from_request(req, self.args['name'])
      if data_path:
        return {self.args['name']: data_path}
    return super().prepare(req)

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      return re.match(re_full(self.args['constraint']), self.args['value'])

  @property
  def value(self):
    ret = super().value
    if ret is None: return ''
    else: return ret

  def to_cwl(self):
    schema = super().to_cwl()
    schema['type'] = f"File{'' if self.args.get('required') == True else '?'}"
    return schema

  def to_cwl_value(self):
    if not self.args['value']:
      return None
    uri_parsed = URI(self.args['value'])
    name = uri_parsed.fragment or self.args['value']
    path = str(uri_parsed.with_fragment(None))
    return {
      'class': 'File',
      'path': path,
      'name': name,
    }

  def to_jsonschema(self):
    schema = super().to_jsonschema()
    if self.args.get('constraint'): schema['pattern'] = re_full(self.args['constraint'])
    return schema

  @property
  def public_url(self):
    try:
      from flask import request
      return join_routes(request.base_url, self.value)[1:]
    except RuntimeError:
      from appyter.context import get_env
      config = get_env()
      return join_routes(config.get('PUBLIC_URL', 'file:///' + config.get('CWD')), self.value)[1:]

  @property
  def is_file(self):
    return True
