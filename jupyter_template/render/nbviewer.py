import nbformat
import nbconvert
from bs4 import BeautifulSoup

def render_nbviewer_from_nb(env, nb):
  ''' Render an nbviewer (HTML serialization of the notebook)
  '''
  exporter = nbconvert.HTMLExporter()
  export, _ = exporter.from_notebook_node(nb)
  # Strip things from export
  soup = BeautifulSoup(export, 'html.parser')
  soup.find('meta').decompose()  # remove meta
  soup.find('title').decompose()  # remove title
  # remove first 2 scripts (require.js and jquery)
  soup.find('script').decompose()
  soup.find('script').decompose()
  # soup.find('style').decompose() # remove first style (bootstrap)
  soup.find('link').decompose()  # remove link to custom stylesheet
  nb_container = soup.select('#notebook-container')[0]
  nb_container['class'] = ''
  nb_container['id'] = ''
  return str(soup)
