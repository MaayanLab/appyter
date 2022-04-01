from flask import current_app
from appyter.ext.urllib import join_url, parent_url

async def get_user_config(data):
  if not data.get('_auth'): raise PermissionError
  import aiohttp
  async with aiohttp.ClientSession(
    headers={
      'Authorization': f"Bearer {data['_auth']}",
    },
    raise_for_status=True,
  ) as session:
    async with session.post(
      join_url(
        parent_url(data['_config']['PUBLIC_URL']),
        'postgrest/rpc/user_config',
      ),
      json={ 'config': None },
    ) as res:
      return await res.json()
