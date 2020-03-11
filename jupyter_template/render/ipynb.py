import nbformat as nbf
from copy import deepcopy
from jupyter_template.parse.nbtemplate import cell_match

def render_cell(env, cell):
  if cell.cell_type == 'code':
    cell.outputs = []
    cell['execution_count'] = None

  cell_m = cell_match.match(cell.source)
  if cell_m:
    line = cell_m.group('type').strip()
    cell_source = cell_m.group('source').strip()

    if line == 'init':
      return None

    template = env.from_string(cell_source)
    rendered = '\n'.join(
      line
      for line in template.render().splitlines()
      if line.strip() != ''
    )

    # Variables added via jinja should get added to globals
    #  for subsequent evaluation
    for k, v in template.module.__dict__.items():
      if not k.startswith('_'):
        env.globals[k] = v

    # Alter cell render based on line
    if line == 'markdown':
      cell = nbf.v4.new_markdown_cell(rendered)
    elif 'hide' in line.split('_') or rendered == '':
      cell = None
    else:
      cell = nbf.v4.new_code_cell(rendered)

  return cell


def render_nb_from_nbtemplate(env, nb):
  nb = deepcopy(nb)
  nb.cells = list(filter(None, [
    render_cell(
      env,
      cell,
    )
    for cell in nb.cells
  ]))
  return nb
