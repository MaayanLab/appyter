from appyter.ext.urllib import join_url, parent_url

async def get_user_config(auth=None, config=None):
  if not auth: raise PermissionError
  import aiohttp
  async with aiohttp.ClientSession(
    headers={
      'Authorization': f"Bearer {auth}",
    },
    raise_for_status=True,
  ) as session:
    async with session.post(
      join_url(
        parent_url(config['PUBLIC_URL']),
        'postgrest/rpc/user_config',
      ),
      json=dict(config=None),
    ) as res:
      return await res.json()
