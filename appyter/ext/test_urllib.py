from appyter.ext.urllib import URI
from appyter.ext.pytest import assert_eq

def test_uri_trailing_slash():
  ''' servers may treat `/a/` and `/a` differently (e.g. GEO's download endpoint), so we preserve it
  '''
  for url in [
    'https://www.ncbi.nlm.nih.gov/geo/download/?acc=GSE152418&format=file',
    'https://example.com/a/b/',
    'https://example.com/a/b',
  ]:
    assert_eq(str(URI(url)), url)
  assert_eq(
    str(URI('https://example.com/a/?q=1').with_fragment('file.txt')),
    'https://example.com/a/?q=1#file.txt',
  )
