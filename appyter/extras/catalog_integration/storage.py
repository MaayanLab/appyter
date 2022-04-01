import re

from appyter.ext.fsspec.core import url_to_chroot_fs
from appyter.ext.urllib import join_slash
from appyter.extras.catalog_integration.user_config import get_user_config
from appyter.ext.asyncio.helpers import ensure_sync

def prepare_storage(data):
  # parse storage
  if data.get('_storage'):
    # cavatica storage provider, obtain CAVATICA API Key and instantiate sbfs
    m = re.match(r'^cavatica://(?P<user>[a-z0-9_-]+)/(?P<project>[a-z0-9_-]+)/?$', data['_storage'])
    if m:
      cavatica_opts = m.groupdict()
      if not data.get('_auth'): raise PermissionError
      user_config = ensure_sync(get_user_config(data['_auth']))
      if not user_config.get('cavatica_api_key'): raise PermissionError
      return url_to_chroot_fs(
        join_slash(
          f"writecache::chroot::sbfs://{cavatica_opts['user']}/{cavatica_opts['project']}/appyter/output",
          data.get('_id', ''),
        ),
        sbfs=dict(
          auth_token=user_config['cavatica_api_key'],
        ),
      )
    else:
      raise NotImplementedError
