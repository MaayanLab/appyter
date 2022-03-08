# Appyter
This module enables you to turn your jupyter notebook into a jinja2 template-driven web application. Or just parse for other purposes.

## Installation
NOTE: This application uses modern python features including async await (3.5) and fstrings (3.6), to ensure you have the best experience please use python >= 3.8.

```bash
# Install package from pip
pip3 install --upgrade appyter

# OR Install package from github repository main
pip3 install --upgrade git+https://github.com/Maayanlab/appyter.git
```

## Usage
Appyter enables you to serve that notebook on an executable webapp.

`appyter jupyter_notebook.ipynb`

If for some reason, `appyter` doesn't end up discoverable in your PATH, you can use `python3 -m appyter` instead.

- A dotenv file (`.env`) or environment variables can be use to configure HOST, PORT, and PREFIX of the webserver.
- Some pre-configured profiles can be used for styling the form (`--profile=profile_name`) see `appyter/profiles`
- In debug mode (`--debug`), changes to the notebook will automatically update the webapp.
- Custom fields can be used by putting them in the directory of execution with the following format:
  - `./fields/YourField.py`: Python Field Implementation
- The templates used natively by the application can be modified to provide your own look and feel:
  - `./templates/head.jinja2`: Custom head (title, CSS, scripts)
  - `./templates/form.jinja2`: Custom form handling
  - `./templates/fields/StringField.jinja2`: Override field style
- Custom jinja2 filters can be added if necessary
  - `./filters/your_filter.py`: Python jinja2 filter (function)
- Custom externally-referenced resources (i.e. images) can be put under the static directory
  - `./static/img/your_image.png`: Reference in templates with `{% static 'img/your_image.png' %}`
- Custom blueprints to additionally mount with flask
  - `./blueprints/your_app/__init__.py`: `your_app = Blueprint('your_app', __name__)`


## Creating an Appyter

Create a standard python jupyter notebook, make the first cell:
```
#%%appyter init
from appyter import magic
magic.init(lambda _=globals: _())
```

Normal cells are allowed, you also have access to jinja2-rendered cells:
```
%%appyter {cell_type}
```

Supported cell_types:
- `markdown`: Substitute jinja2 template variables, render as a markdown cell
- `hide`: Substitute jinja2 template variables, show it rendered in your notebook with the default values, but when executing publicly, don't show/execute the cell.
- `code_exec`: Substitute jinja2 template variables, render as python, show it rendered in your notebook with the default values and execute it
- `code_eval`: Substitute jinja2 template variables, render as python, show it rendered in your notebook with the default values and execute it, "eval" the last line of the cell and display the result.

## Discussion
Consider the following notebook:

```
%%appyter markdown
# {{ StringField(name='title', label='Title', default='My Title').render_value }}

{{ TextField(name='description', label='Description', default='My description').render_value }}
```

```
%%appyter code_eval
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
assert parse_variables(appyter) == {
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
assert render_jupyter(appyter, {
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
assert render_html(appyter) == '''
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
<script src="./appyter.js"></script>
<script>
  document.getElementById("notebook").on('submit', appyter.submit)
</script>
'''

# Web UI Renderer
assert render_html_renderer(appyter, {
  'title': 'Test',
  'description': '',
  'number_1': 0,
  'number_2': 5,
  'operator': 'subtract',
}) == '''
<div id="notebook"></div>
<script src="./appyter.js"></script>
<script>
  document.on('load', function () {
    appyter.render(
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

`appyter` can be used to get these conversions, it can also be used to host standalone webapps using these mechanisms.

## Development

### Testing

`pytest` is used for python testing. It can be invoked as follows:

```bash
# it is also prudent to test other protocols such as s3 (production) & sbfs (CAVATICA)
export FSSPEC_URI='memory://'
pytest --log-cli-level=DEBUG appyter
```
