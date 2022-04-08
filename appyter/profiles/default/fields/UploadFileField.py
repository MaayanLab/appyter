import re
from appyter.fields import Field
from appyter.ext.flask import secure_filepath, join_routes
from appyter.ext.re import re_full
from appyter.ext.yarl import URLEx
from appyter.render.flask_app.upload import upload_from_request

class UploadFileField(Field):
  ''' Represing a uploadable File and facilitating that file upload.
  The field ends up being a string of the file path, for example:
  ```python
  import pandas as pd
  df = pd.read_csv({{ UploadFileField(name='my-csv', label='My CSV') }})
  ```

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param constraint: A regular expression for validating the file name.
  :param required: (Optional[bool]) Whether or not this field is required (defaults to false)
  :param default: (str) A default value as an example and for use during prototyping
  :param examples: (Optional[Dict[str, str]]) Named url paths to example files to upload
    paths can be relative i.e. `{ "my_file.txt": url_for('static', filename='my_file.txt') }`, or a remote url.
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, constraint=r'.*', **kwargs):
    super().__init__(
      constraint=constraint,
      **kwargs,
    )

  @property
  def raw_value(self):
    if type(self.args['value']) == str and self.args['value']:
      uri_parsed = URLEx(self.args['value'])
      filename = uri_parsed.fragment or self.args['value']
      if self._env.globals['_config']['SAFE_MODE']:
        return secure_filepath(filename)
      else:
        return filename
    else:
      return None

  def prepare(self, req):
    if getattr(req, 'files', None):
      data_path = upload_from_request(req, self.args['name'])
      if data_path:
        return {self.args['name']: data_path}
    return super().prepare(req)

  def constraint(self):
    if self.raw_value is None:
      return not self.args.get('required')
    else:
      return re.match(re_full(self.args['constraint']), self.raw_value)

  def to_cwl(self):
    schema = super().to_cwl()
    schema['type'] = f"File{'' if self.args.get('required') == True else '?'}"
    return schema

  def to_cwl_value(self):
    if not self.args['value']:
      return None
    uri_parsed = URLEx(self.args['value'])
    name = uri_parsed.fragment or self.args['value']
    path = str(uri_parsed.with_fragment(None))
    return {
      'class': 'File',
      'path': path,
      'name': name,
    }

  def to_click(self):
    import click
    args, kwargs = super().to_click()
    kwargs['type'] = click.Path()
    return args, kwargs

  @property
  def value(self):
    ret = super().value
    if ret is None: return ''
    else: return ret

  @property
  def public_url(self):
    try:
      from flask import request
      return join_routes(request.base_url, self.value)[1:]
    except RuntimeError:
      from appyter.context import get_env
      config = get_env()
      return join_routes(config.get('PUBLIC_URL', 'file:///' + config.get('CWD')), self.value)[1:]