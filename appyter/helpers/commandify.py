import click

from appyter.cli import cli
from appyter.ext.click import click_argument_setenv

def ipynb_options_from_sys_argv(func):
  import sys
  if len(sys.argv) >= 3 and sys.argv[1] == 'commandify' and sys.argv[2][0] != '-':
    import os
    import fsspec
    import functools
    from appyter.context import get_env_from_kwargs, get_jinja2_env
    from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
    from appyter.ext.dict import dict_filter_none
    from appyter.parse.nb import nb_from_ipynb_io
    from appyter.ext.asyncio.event_loop import with_event_loop
    from appyter.ext.urllib import parent_url
    #
    ipynb = sys.argv[2]
    cwd = parent_url(ipynb) or os.cwd
    #
    with with_event_loop():
      with fsspec.open(ipynb, 'r') as fr:
        nbtemplate = nb_from_ipynb_io(fr)
    #
    env = get_jinja2_env(
      config=get_env_from_kwargs(cwd=cwd, ipynb=ipynb, mode='inspect'),
    )
    fields = list(dict_filter_none({
      field.args['name']: field.to_click()
      for field in parse_fields_from_nbtemplate(env, nbtemplate, deep=True)
    }).values())
    for field in fields:
      func = click.option(*field[0], **field[1])(func)
    #
    @functools.wraps(func)
    def wrapper(**kwargs):
      with with_event_loop():
        return func(dict(cwd=cwd, ipynb=ipynb, nbtemplate=nbtemplate), **kwargs)
    return wrapper
  return func

@cli.group(help='Construct an operable command-line from an appyter')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def commandify(ipynb=None):
  pass

@commandify.command(help='Construct a notebook from an appyter and its arguments')
@click.option('-o', type=str, metavar='FILE', default='-', help='Output notebook')
@ipynb_options_from_sys_argv
def nbconstruct(ctx, o=None, **kwargs):
  if o == '-': o = '/dev/stdout'
  import fsspec
  from appyter.context import get_env, get_jinja2_env
  from appyter.render.nbconstruct import render_nb_from_nbtemplate
  from appyter.parse.nb import nb_to_ipynb_io
  env = get_jinja2_env(
    config=get_env(ipynb=ctx['ipynb'], mode='construct'),
    context=kwargs,
  )
  nb = render_nb_from_nbtemplate(env, ctx['nbtemplate'], data=kwargs)
  with fsspec.open(o, 'w') as fw:
    nb_to_ipynb_io(nb, fw)

@commandify.command(help='Construct and execute an appyter')
@click.option('-s', type=str, metavar='FILE', default='-', help='Status output')
@click.option('-o', type=str, metavar='FILE', default='-', help='Output notebook')
@ipynb_options_from_sys_argv
def run(ctx, s=None, o=None, **kwargs):
  if s == '-': s = '/dev/stderr'
  if o == '-': o = '/dev/stdout'
  import fsspec
  import shutil
  from appyter.context import get_env, get_jinja2_env
  from appyter.ext.asyncio.helpers import ensure_sync
  from appyter.parse.nb import nb_to_ipynb_io
  from appyter.render.nbconstruct import render_nb_from_nbtemplate
  from appyter.render.nbexecute import nbexecute_async, json_emitter_factory
  from appyter.ext.tempfile import tempdir
  # render notebook
  env = get_jinja2_env(
    config=get_env(cwd=ctx['cwd'], ipynb=ctx['ipynb'], mode='construct'),
    context=kwargs,
  )
  nb = render_nb_from_nbtemplate(env, ctx['nbtemplate'], data=kwargs)
  # write into temporary directory
  with tempdir() as tmp_dir:
    with (tmp_dir/ctx['ipynb']).open('w') as fw:
      nb_to_ipynb_io(nb, fw)
    # execute notebook, sending status updates to `s`
    with fsspec.open(s, 'w') as fw:
      ensure_sync(nbexecute_async(
        cwd=str(tmp_dir),
        ipynb=ctx['ipynb'],
        emit=json_emitter_factory(fw),
        fuse=False,
      ))
    # write output notebook, to `o`
    with (tmp_dir/ctx['ipynb']).open('r') as fr:
      with fsspec.open(o, 'w') as fw:
        shutil.copyfileobj(fr, fw)
