from appyter.ext.contextlib import ensure_context
from appyter.ext.asyncio.helpers import ensure_async

@ensure_async
def fsspec_read_and_run(path, op):
  from appyter.ext.fsspec.core import url_to_fs_ex
  fs, fo = url_to_fs_ex(path)
  with ensure_context(fs) as fs:
    with fs.open(fo, 'r') as fr:
      return op(fr)

@ensure_async
def fsspec_cp(left_fs, left_fo, right_fs, right_fo):
  import shutil
  from appyter.ext.urllib import parent_url
  with left_fs.open(left_fo, 'rb') as fr:
    right_fs.makedirs(parent_url(right_fo), exist_ok=True)
    with right_fs.open(right_fo, 'wb') as fw:
      shutil.copyfileobj(fr, fw)
