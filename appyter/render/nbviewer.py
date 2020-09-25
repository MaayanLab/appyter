import nbconvert
from bs4 import BeautifulSoup

def find_and_decompose(soup, obj):
  el = soup.find(obj)
  if el:
    el.decompose()

def render_nbviewer_from_nb(env, nb):
  ''' Render an nbviewer (HTML serialization of the notebook)
  '''
  exporter = nbconvert.HTMLExporter()
  export, _ = exporter.from_notebook_node(nb)
  # Strip things from export
  soup = BeautifulSoup(export, 'html.parser')
  find_and_decompose(soup, 'meta')  # remove meta
  find_and_decompose(soup, 'title')  # remove title
  # remove first 2 scripts (require.js and jquery)
  find_and_decompose(soup, 'script')
  find_and_decompose(soup, 'script')
  # find_and_decompose(soup, 'style') # remove first style (bootstrap)
  find_and_decompose(soup, 'link')  # remove link to custom stylesheet
  nb_container = soup.select('#notebook-container')[0]
  nb_container['class'] = ''
  nb_container['id'] = ''
  return str(soup)
