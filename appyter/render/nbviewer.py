import nbconvert
from bs4 import BeautifulSoup

def render_nbviewer_from_nb_soup(env, nb):
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
  return soup

def render_nbviewer_cell_from_nb(env, nb, cell_index):
  ''' Render a single cell from a notebook

  TODO: Surely this can be more efficient..
  '''
  exporter = nbconvert.HTMLExporter()
  export, _ = exporter.from_notebook_node(nb)
  soup = BeautifulSoup(export, 'html.parser')
  return soup.select('.cell')[cell_index]

def render_nbviewer_from_nb(env, nb):
  ''' Render an nbviewer (HTML serialization of the notebook)
  '''
  soup = render_nbviewer_from_nb_soup(env, nb)
  nb_container = soup.select('#notebook-container')[0]
  nb_container['class'] = ''
  nb_container['id'] = ''
  return str(soup)

def render_nb_from_stream(env, stream):
  ''' Render a jupyter notebook and update it *in* a jupyter notebook from an nbexecute progress stream.

  :param nb: (ipynb) The loaded jupyter notebook
  :param stream: (generator) The stream of messages coming from nbexecute.
  '''
  import json
  import uuid
  from IPython.display import display, update_display, HTML
  from appyter.util import try_json_loads
  from appyter.parse.nb import nb_from_json
  id = '_' + str(uuid.uuid4())
  nb = None
  display(HTML('Starting...'), display_id=id+'_status')
  for msg in stream:
    msg = try_json_loads(msg)
    if type(msg) == dict:
      if nb is None and msg['type'] == 'nb':
        # received the constructed notebook parse and render it
        nb = msg['data']
        nb_html = render_nbviewer_from_nb_soup(env, nb_from_json(nb))
        nb_html.select('#notebook-container')[0]['id'] = '#' + id
        # show each cell separately with an id based on the index
        for cell_index, cell in enumerate(nb_html.select('.cell')):
          display(HTML(str(cell)), display_id=id+'_%d' % (cell_index))
      elif nb is not None and msg['type'] == 'cell':
        cell, cell_index = msg['data']
        # when a cell updates, we'll update the notebook and update the cell display
        nb['cells'][cell_index] = cell
        cell_rendered = str(render_nbviewer_cell_from_nb(env, nb_from_json(nb), cell_index))
        update_display(HTML(cell_rendered), display_id=id+'_%d' % (cell_index))
      elif msg['type'] == 'status':
        update_display(HTML(str(msg['data'])), display_id=id+'_status')
      elif msg['type'] == 'error':
        update_display(HTML('Error'), display_id=id+'_status')
        raise Exception(msg['data'])
    else:
      update_display(HTML(str(msg)), display_id=id+'_status')
  update_display(HTML(''), display_id=id+'_status')
  #
  return nb
