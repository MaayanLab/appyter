import re
from appyter.extras.catalog_integration.user_config import get_user_config

async def prepare_executor(data):
  ''' Safely translate public facing executor URI into internally operable execspec URIs
  '''
  # if executor hints are provided (e.g. ['executor:default'])
  #  we'll verify that the chosen executor is supported
  executor_hints = {
    hint_value
    for hint in data.get('_config').get('HINTS', set())
    for hint_prefix, sep, hint_value in (hint.partition(':'),)
    if hint_prefix == 'executor' and sep == ':'
  }
  if executor_hints and data.get('_executor', 'default') not in executor_hints:
    raise Exception('Executor not supported for this appyter')
  #
  if data.get('_executor'):
    if data['_executor'] == 'cavatica':
      user_config = await get_user_config(data.get('_auth'), data.get('_config'))
      if not user_config.get('cavatica_api_key'): raise PermissionError
      assert re.match(r'^[0-9a-f]+$', user_config['cavatica_api_key']) is not None, 'Malformed CAVATICA API Key'
      m = re.match(r'^cavatica://(?P<user>[a-z0-9_-]+)/(?P<project>[a-z0-9_-]+)$', data['_storage'])
      if m:
        return f"cavatica#?cwl=appyter.cwl&project={m.group('user')}/{m.group('project')}&auth_token={user_config['cavatica_api_key']}"
      else:
        raise Exception('Unsupported storage URI')
