from flask import current_app
from appyter.ext.urllib import join_url, parent_url

async def get_user_config(auth):
  import aiohttp
  async with aiohttp.ClientSession(
    headers={
      'Authorization': auth
    },
    raise_for_status=True,
  ) as session:
    async with session.post(
      join_url(
        parent_url(current_app.config['PUBLIC_URL']),
        'postgrest/rpc/user_config',
      )
    ) as res:
      return await res.json()
