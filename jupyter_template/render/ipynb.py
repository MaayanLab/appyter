import json
import nbformat as nbf

def render_cell(env, cell):
  from jupyter_template.parse.nbtemplate import cell_match

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


def render_notebook(env, nb):
  nb.cells = [
    cell
    for cell in [
      render_cell(
        env,
        cell,
      )
      for cell in nb.cells
    ]
    if cell is not None
  ]
  return nb


def render_ipynb(env, ipynb):
  nb = nbf.read(ipynb, as_version=4)
  return render_notebook(
    env,
    nbf.reads(ipynb, as_version=4)
  )


def render_ipynb_file(env, filename):
  return render_notebook(
    env,
    nbf.read(open(filename, 'r'), as_version=4)
  )
