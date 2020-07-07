import nbformat as nbf
from copy import deepcopy
from appyter.parse.nbtemplate import cell_match

def render_cell(env, cell):
  ''' Render a single cell, calling jinja2 templates when necessary
  (only on %%appyter -matched cells) and converting cells
  to markdown / removing them as necessary.
  '''
  if cell.cell_type == 'code':
    cell.outputs = []
    cell['execution_count'] = None

  cell_m = cell_match.match(cell.source)
  if cell_m:
    cell_type = cell_m.group('type').strip().split('_')
    cell_source = cell_m.group('source').strip()

    if cell_type == ['init']:
      return None

    template = env.from_string(cell_source)
    rendered = template.render()
    trimmed = '\n'.join(
      line
      for line in rendered.splitlines()
      if line.strip() != ''
    )

    # Variables added via jinja should get added to globals
    #  for subsequent evaluation
    for k, v in template.module.__dict__.items():
      if not k.startswith('_'):
        env.globals[k] = v

    # Alter cell render based on cell_type
    if cell_type == ['markdown']:
      cell = nbf.v4.new_markdown_cell(rendered)
    elif 'hide' in cell_type or not trimmed:
      cell = None
    else:
      cell = nbf.v4.new_code_cell(trimmed)

  return cell


def render_nb_from_nbtemplate(env, nb):
  ''' Render the notebook by rendering the jinja2 templates using the context in env.
  '''
  nb = deepcopy(nb)
  nb.cells = list(filter(None, [
    render_cell(
      env,
      cell,
    )
    for cell in nb.cells
  ]))
  return nb
