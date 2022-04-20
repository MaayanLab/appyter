''' IPython magic for making templating easy~. This basically
just allows our jinja-type language to be executed in place
injecting the defaults into the environment so we can easily
debug the notebook at the same time as building the appyter.

The same call structure is used during preprocess and at runtime
but performing different tasks--this way setting up a notebook is
as simple as running it with different nbtemplate's being provided
for import.

Usage (put the following in the first cell):

```python
#%%appyter init
from appyter import magic
magic.init(lambda _=globals: _())
```
'''

'''
Setup given globals
'''
def init(_globals, verbose=False, ipynb='app.ipynb', mode='magic', safe_mode=False, **kwargs):
  ''' Initialize appyter magic.

  Sets up a jinj2 environment and injects %%appyter magic into your environment.
  
  :param _globals: (Dict[str, Any]) A callable with your globals for the purpose of injection, basically just: `lambda _=globals: _()`
  :param verbose: (Optional[bool]) Expand exception reporting to be more verbose
  '''
  import os
  import jinja2
  import jinja2.meta
  import traceback
  from appyter.context import get_env, get_jinja2_env
  env = get_jinja2_env(config=get_env(verbose=verbose, ipynb=ipynb, mode=mode, safe_mode=safe_mode, **kwargs))
  from IPython.core.magic import register_cell_magic
  from IPython.display import display, Markdown, HTML

  '''
  register_cell_magic allows function to execute an entire cell with the following call structure:
  ```python
  %%my_magic whatever
  all
  my
  data
  ```
  Results in a call:
  ```python
  my_magic(
    "whatever",
    """all
    my
    data"""
  )
  ```
  '''

  @register_cell_magic
  def appyter(line, cell):
    ''' Appyter Cell Magic: See Steps for more information.
    Compile jinja2 into source code, and then evaluate that
    source code.
    '''

    '''
    Step 1. Render cell with jinja2, removing empty lines.
    execute or display the results, modifying a copy of the
    current python globals dict.
    '''
    global_internal = _globals()
    cell_type = line.split('_')
    try:
      cell_lines = cell.splitlines()
      try:
        undeclared = jinja2.meta.find_undeclared_variables(env.parse(cell))
        if undeclared:
          for lineno, cell_line in enumerate(cell_lines):
            if any(v in cell_line for v in undeclared):
              display(HTML(f"<div style='color: red'>{lineno}: {cell_line}</div>"))
          raise Exception(f"undeclared variable(s) {undeclared}")
        template = env.from_string(cell)
        template_rendered = template.render()
      except Exception as e:
        if getattr(e, 'lineno', None) is not None:
          display(HTML(f"<div style='color: red'>{e.lineno}: {cell_lines[e.lineno-1]}</div>"))
        raise e
      #
      rendered_template_lines = list(filter(None, map(str.rstrip, template_rendered.splitlines())))
      try:
        if len(rendered_template_lines) > 0:
          if cell_type == ['markdown']:
            display(Markdown(template_rendered))
          elif 'code' in cell_type:
            rendered = '\n'.join(rendered_template_lines[:-1])
            rendered_last = rendered_template_lines[-1]
            display(Markdown('```python\n%s\n```' % ('\n'.join((rendered, rendered_last)))))
            #
            if 'eval' in cell_type:
              exec(rendered, global_internal)
              #
              try:
                display(eval(rendered_last, global_internal))
              except Exception as e:
                setattr(e, 'lineno', len(rendered_template_lines))
                raise e
            elif 'exec' in cell_type:
              exec('\n'.join((rendered, rendered_last)), global_internal)
          else:
            raise Exception('Unrecognized appyter cell_type')
        #
      except Exception as e:
        if getattr(e, 'lineno', None) is not None:
          display(HTML(f"<div style='color: red'>{e.lineno}: {rendered_template_lines[e.lineno-1]}</div>"))
        raise e
    except Exception as e:
      display(HTML(f"<div style='color: red'>Error: {e}</div>"))
      if verbose:
        traceback.print_exc()
      return
    '''
    Step 2. Check for new variables in the internal global
    and pass them to the python global scope. Check for
    new variables in the jinja2 template and pass them to the
    template environment global so they are available in
    future jinja2 calls.
    '''
    for k, v in global_internal.items():
      if not k.startswith('_'):
        _globals()[k] = v

    for k, v in template.module.__dict__.items():
      if not k.startswith('_'):
        env.globals[k] = v
