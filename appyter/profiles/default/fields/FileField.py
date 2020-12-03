import re
import logging
logger = logging.getLogger(__name__)

from appyter.fields import Field
from appyter.util import secure_filepath, join_routes, collapse

class FileField(Field):
  ''' Represing a uploadable File and facilitating that file upload.
  The field ends up being a string of the file path, for example:
  ```python
  import pandas as pd
  df = pd.read_csv({{ FileField(name='my-csv', label='My CSV') }})
  ```

  :param name: (str) A name that will be used to refer to the object as a variable and in the HTML form.
  :param label: (str) A human readable label for the field for the HTML form
  :param description: (Optional[str]) A long human readable description for the field for the HTML form
  :param constraint: A regular expression for validating the file name.
  :param default: (str) A default value as an example and for use during prototyping
  :param examples: (Optional[Dict[str, str]]) Named url paths to example files to upload
    paths can be relative i.e. `{ "my_file.txt": url_for('static', filename='my_file.txt') }`, or a remote url.
  :param section: (Optional[str]) The name of a SectionField for which to nest this field under, defaults to a root SectionField
  :param value: (INTERNAL Any) The raw value of the field (from the form for instance)
  :param \**kwargs: Remaining arguments passed down to :class:`appyter.fields.Field`'s constructor.
  '''
  def __init__(self, constraint=r'.*', examples={}, **kwargs):
    super().__init__(
      constraint=constraint,
      examples=examples,
      **kwargs,
    )

  def prepare(self, req):
    logger.debug(f"prepare")
    # TODO: maybe we should be turning the contents of the field into a file?
    if type(req) == dict:
      return {self.args['name']: req.get(self.args['name'])}
    elif req.json:
      return {self.args['name']: req.json.get(self.args['name'])}
    elif req.form:
      from appyter.render.flask_app.download import upload_from_request
      return dict(
        {self.args['name']: collapse(req.form.getlist(self.args['name']))},
        **upload_from_request(req, self.args['name'])
      )
    else:
      raise NotImplementedError

  def pre_construct(self, ctx, **kwargs):
    logger.debug(f"pre_construct")
    from appyter.render.flask_app.util import sanitize_sha1sum
    if fdata := ctx.get(self.args['name']):
      content_hash, filename = fdata.split('/', maxsplit=1)
      content_hash = sanitize_sha1sum(content_hash)
      filename = secure_filepath(filename)
      return {
        self.args['name']: filename,
        f"__{self.args['name']}__orig": fdata,
      }
    #
    return {}

  def post_construct(self, ctx, data_fs=None, results_path=None, **kwargs):
    logger.debug(f"post_construct")
    from appyter.ext.fs import Filesystem
    from appyter.render.flask_app.util import sanitize_sha1sum
    if fdata := ctx.get(f"__{self.args['name']}__orig"):
      content_hash, filename = fdata.split('/', maxsplit=1)
      content_hash = sanitize_sha1sum(content_hash)
      data_fs.link(
        Filesystem.join('input', content_hash),
        Filesystem.join(results_path, filename)
      )

  @property
  def raw_value(self):
    if type(self.args['value']) == str:
      return secure_filepath(self.args['value'])
    else:
      return None

  def constraint(self):
    return self.raw_value is not None and re.match(self.args['constraint'], self.raw_value)

  @property
  def public_url(self):
    try:
      from flask import request
      return join_routes(request.base_url, self.value)[1:]
    except:
      from appyter.context import get_env
      config = get_env()
      return join_routes(config.get('PUBLIC_URL', 'file:///' + config.get('CWD')), self.value)[1:]
