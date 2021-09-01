import json
import nbformat as nbf

def nb_from_ipynb_string(string):
  return nbf.reads(string, as_version=4)

def nb_from_ipynb_io(io):
  return nbf.read(io, as_version=4)

def nb_from_json(j):
  return nb_from_ipynb_string(json.dumps(j))

def nb_to_ipynb_string(nb):
  return nbf.writes(nb)

def nb_to_ipynb_io(nb, io):
  # remove `id` when writing, this is added by nbclient
  #  but causes nbformat validation errors when reading.
  for cell in nb.cells:
    if 'id' in cell:
      del cell['id']
  return nbf.write(nb, io)

def nb_to_json(nb):
  return json.loads(nb_to_ipynb_string(nb))
