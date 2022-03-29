import re

from jupyterlab_server import slugify
from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.extras.catalog_integration.user_config import get_user_config
from appyter.ext.asyncio.helpers import ensure_sync

def prepare_storage(id, data):
  user_config = None
  # when using cavatica executor, default to sbfs for cavatica project
  if data.get('_executor') == 'cavatica':
    if not data.get('_auth'): raise PermissionError
    if user_config is None: user_config = ensure_sync(get_user_config(data['_auth']))
    if not data.get('_storage'):
      if not user_config.get('cavatica_api_key'): raise PermissionError
      if user_config.get('cavatica_project'):
        return url_to_chroot_fs(
          f"writecache::chroot::sbfs://{slugify(user_config['cavatica_project'])}/appyter/output/{id}",
          sbfs=dict(
            auth_token=user_config['cavatica_api_key'],
          ),
        )
  # parse storage
  if data.get('_storage'):
    # cavatica storage provider, obtain CAVATICA API Key and instantiate sbfs
    m = re.match(r'^cavatica://(?P<user>[a-z0-9_-]+)/(?P<project>[a-z0-9_-]+)/?$', data['_storage'])
    if m:
      cavatica_opts = m.groupdict()
      if not data.get('_auth'): raise PermissionError
      if user_config is None: user_config = ensure_sync(get_user_config(data['_auth']))
      if not user_config.get('cavatica_api_key'): raise PermissionError
      return url_to_chroot_fs(
        f"writecache::chroot::sbfs://{cavatica_opts['user']}/{cavatica_opts['project']}/appyter/output/{id}",
        sbfs=dict(
          auth_token=user_config['cavatica_api_key'],
        ),
      )
    else:
      raise NotImplementedError
