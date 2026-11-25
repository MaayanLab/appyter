import os
from appyter.ext.watchfiles.filter import GlobFilter

def test_glob_filter(tmp_path):
  root = str(tmp_path)
  f = GlobFilter(root, include_file_glob=['*.py'], include_dir_glob=['filters', 'blueprints'], exclude_file_glob=[], exclude_dir_glob=[])
  assert f(None, os.path.join(root, 'filters', 'a.py'))
  assert f(None, os.path.join(root, 'b.py'))
  assert not f(None, os.path.join(root, 'filters', 'a.txt'))
  assert not f(None, os.path.join(root, 'other', 'a.py'))
  assert not f(None, os.path.join(root, '..', 'a.py'))
  f = GlobFilter(root, include_file_glob=['*'], include_dir_glob=['*'], exclude_file_glob=['*.py'], exclude_dir_glob=['data'])
  assert f(None, os.path.join(root, 'templates', 'x', 'form.j2'))
  assert not f(None, os.path.join(root, 'data', 'x', 'out.csv'))
  assert not f(None, os.path.join(root, 'x.py'))
  f = GlobFilter(root, include_file_glob=['*'], include_dir_glob=['*'], exclude_file_glob=[], exclude_dir_glob=[os.path.join(root, 'data')])
  assert not f(None, os.path.join(root, 'data', 'out.csv'))
