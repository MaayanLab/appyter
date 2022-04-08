from dataclasses import dataclass, asdict
from appyter.ext.urllib import join_url, parent_url

@dataclass(frozen=True,)
class FileInfo:
  file: str
  filename: str
  metadata: dict = None

async def add_file(data: FileInfo, auth=None, config=None):
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
        'postgrest/rpc/add_file',
      ),
      json=asdict(data),
    ) as res:
      return await res.json()