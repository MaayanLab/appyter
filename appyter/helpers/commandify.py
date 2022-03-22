import click
import pathlib

from appyter.cli import cli
from appyter.ext.click import click_argument_setenv

def ipynb_options_from_sys_argv(func):
  import sys
  if len(sys.argv) >= 3 and sys.argv[1] == 'commandify' and sys.argv[2][0] != '-':
    import os
    import fsspec
    import functools
    from appyter.context import get_env, get_jinja2_env
    from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
    from appyter.ext.dict import dict_filter_none
    from appyter.parse.nb import nb_from_ipynb_io
    from appyter.ext.asyncio.event_loop import with_event_loop
    #
    arg = pathlib.Path(sys.argv[2])
    assert arg.exists()
    ipynb = arg.name
    cwd = arg.parent.absolute()
    #
    with with_event_loop():
      with fsspec.open(str(cwd / ipynb), 'r') as fr:
        nbtemplate = nb_from_ipynb_io(fr)
    #
    env = get_jinja2_env(
      config=get_env(cwd=str(cwd), ipynb=ipynb, mode='inspect', safe_mode=False),
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
        return func(dict(cwd=str(cwd), ipynb=ipynb, nbtemplate=nbtemplate), **kwargs)
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
    config=get_env(cwd=ctx['cwd'], ipynb=ctx['ipynb'], mode='construct'),
    context=kwargs,
  )
  nb = render_nb_from_nbtemplate(env, ctx['nbtemplate'], data=kwargs)
  with fsspec.open(o, 'w') as fw:
    nb_to_ipynb_io(nb, fw)

@commandify.command(help='Construct and execute an appyter')
@click.option('-s', type=str, metavar='URI', default='file:///dev/stderr', help='Status stream')
@click.option('-e', type=str, metavar='URI', default='local', help='Executor')
@click.option('-o', type=str, metavar='FILE', default=None, help='Output notebook')
@click.option('-w', type=str, metavar='DIR', default=None, help='Working directory')
@ipynb_options_from_sys_argv
def run(ctx, s=None, e=None, o=None, w=None, **kwargs):
  if s == '-':
    s = 'file:///dev/stderr'
  #
  if o is None:
    if w is None:
      o = 'file:///dev/stdout'
  elif o == '-':
    o = 'file:///dev/stdout'
  #
  import fsspec
  import shutil
  from appyter.context import get_env, get_jinja2_env
  from appyter.parse.nb import nb_to_ipynb_io
  from appyter.render.nbconstruct import render_nb_from_nbtemplate
  from appyter.ext.emitter import url_to_emitter
  from appyter.execspec.core import url_to_executor
  from appyter.ext.tempfile import tempdir
  from appyter.ext.asyncio.helpers import ensure_sync
  # render notebook
  env = get_jinja2_env(
    config=get_env(cwd=ctx['cwd'], ipynb=ctx['ipynb'], mode='construct', safe_mode=False),
    context=kwargs,
  )
  nb = render_nb_from_nbtemplate(env, ctx['nbtemplate'], data=kwargs)
  # write into temporary directory
  with tempdir(w) as tmp_dir:
    with (tmp_dir/ctx['ipynb']).open('w') as fw:
      nb_to_ipynb_io(nb, fw)
    # execute notebook, sending status updates to `s`
    with ensure_sync(url_to_emitter(s)) as emitter:
      emitter = ensure_sync(emitter)
      with url_to_executor(e) as executor:
        for msg in executor.run(
          cwd=str(tmp_dir),
          ipynb=ctx['ipynb'],
          fuse=False,
        ):
          emitter(msg)
    # write output notebook, to `o`
    if o:
      with (tmp_dir/ctx['ipynb']).open('r') as fr:
        with fsspec.open(o, 'w') as fw:
          shutil.copyfileobj(fr, fw)
