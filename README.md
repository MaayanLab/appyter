# Jupyter Template

This module enables you to turn your jupyter notebook into a jinja2 template-driven web application. Or just parse `jupyter_templates` for other purposes.

## Usage
Jupyter Template enables you to serve that notebook on an executable webapp.

`jupyter_template jupyter_notebook.ipynb`

- In debug mode (`--debug`), changes to the notebook will automatically update the webapp.
- The application listen uri (`--listen=http://0.0.0.0:80/my_prefix/`) will which ip/port/prefix the app will listen on
- Custom fields can be used by putting them in the directory of execution with the following format:
  - `./fields/YourField.py`: Python Field Implementation
- The templates used natively by the application can be modified to provide your own look and feel:
  - `./templates/head.jinja2`: Custom head (title, CSS, scripts)
  - `./templates/form.jinja2`: Custom form handling
  - `./templates/fields/StringField.jinja2`: Override field style
- Custom externally-referenced resources (i.e. images) can be put under the static directory
  - `./static/img/your_image.png`: Reference in templates with `{% static 'img/your_image.png' %}`
- Custom jinja2 filters can be added if necessary
  - `./filters/your_filter.py`: Python jinja2 filter (function)


## Creating a Jupyter Notebook Template

Create a standard python jupyter notebook, make the first cell:
```
#%%nbtemplate init
from jupyter_template import nbtemplate
nbtemplate.init(lambda _=globals: _())
```

Normal cells are allowed, you also have access to jinja2-rendered cells:
```
%%jupyter_template {cell_type}
```

Supported cell_types:
- `markdown`: Substitute jinja2 template variables, render as a markdown cell
- `code`: Substitute jinja2 template variables, render as python and show it rendered in your notebook with the default values, but don't execute it
- `code_eval`: Substitute jinja2 template variables, render as python, show it rendered in your notebook with the default values and execute it
- `hide_code_eval`: Substitute jinja2 template variables, render as python, show it rendered in your notebook with the default values and execute it, but when executing publicly, don't show the cell.

## Discussion
Consider the following notebook:

```
%%jupyter_template markdown
# {{ StringField(name='title', label='Title') }}

{{ TextField(name='description', label='Description') }}
```

```
%%jupyter_template eval
{% set number_1 = IntField(name='number_1', label='First Number', min=0, max=10, default=5) %}
{% set number_2 = IntField(name='number_2', label='Second Number', min=0, max=10, default=5) %}
{% set op = ChoiceField(
  name='operator',
  label='Operator',
  choices={
    'add': '+',
    'subtract': '-',
    'multiply': '*',
    'divide': '/',
    'power': '**',
  },
  default='add',
) %}
answer = {{ number_1 }} {{ op }} {{ number_2 }}
```

This can be parsed in various ways:

```python
# Parse variables alone
assert parse_variables(notebook_template) == {
  'number_1': IntField(name='number_1', label='First Number', min=0, max=10, default=5),
  'number_2': IntField(name='number_2', label='Second Number', min=0, max=10, default=5),
  'operator': ChoiceField(
    name='operator',
    label='Operator',
    choices={
      'add': '+',
      'subtract': '-',
      'multiply': '*',
      'divide': '/',
      'power': '**'
    },
    default='add'
  ),
}

# Render jupyter notebook with variables substituted
assert render_jupyter(notebook_template, {
  'title': 'Test',
  'description': '',
  'number_1': 0,
  'number_2': 5,
  'operator': 'subtract',
}) == '''
---
# Test

---
answer = 0 - 5
---
''' # in valid ipynb syntax

# Render web UI
assert render_html(notebook_template) == '''
<form id="notebook">
  Title: <input type="string" name="title"></input>
  Description: <textarea name="description"></textarea>
  First Number: <input type="number" name="number_1" min=0 max=10></input>
  Second Number: <input type="number" name="number_2" min=0 max=10></input>
  Operator: <select name="operator">
    <option value="add">add</option>
    <option value="subtract">subtract</option>
    <option value="divide">divide</option>
    <option value="power">power</option>
  </select>
  <input type="submit" text="Submit"></input>
</form>
<script src="./jupyter_template.js"></script>
<script>
  document.getElementById("notebook").on('submit', jupyter_template.submit)
</script>
'''

# Web UI Renderer
assert render_html_renderer(notebook_template, {
  'title': 'Test',
  'description': '',
  'number_1': 0,
  'number_2': 5,
  'operator': 'subtract',
}) == '''
<div id="notebook"></div>
<script src="./jupyter_template.js"></script>
<script>
  document.on('load', function() {
    jupyter_template.render(
      document.getElementById("notebook"),
      {
        "title": "Test",
        "description": "",
        "number_1": 0,
        "number_2": 5,
        "operator": "subtract",
      }
    )
  })
</script>
'''
```

jupyter_template can be used to get these conversions, it can also be used to host standalone webapps using these mechanisms.
