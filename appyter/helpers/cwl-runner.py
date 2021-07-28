import os
import shutil
import sys
import click

from appyter.cli import cli
from appyter.ext.fs import Filesystem
from appyter.context import get_env, get_jinja2_env
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.ext.click import click_argument_setenv
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.nbexecute import nbexecute_async, json_emitter_factory

@cli.command(
  help='Construct and execute an appyter given arguments',
  context_settings=dict(
    ignore_unknown_options=True,
  ),
)
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
@click.pass_context
def cwl_runner(ctx, ipynb):
  context = ctx.args
  cwd = os.path.realpath(os.path.dirname(ipynb))
  ipynb = os.path.realpath(ipynb, cwd)
  env = get_jinja2_env(
    config=get_env(cwd=cwd, ipynb=ipynb, mode='construct'),
    context=context,
  )
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  with Filesystem('tmpfs://') as tmp_fs:
    with tmp_fs.open(ipynb, 'w') as fw:
      nb_to_ipynb_io(nb, fw)
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nbexecute_async(
      cwd=tmp_fs.path(),
      ipynb=tmp_fs.path(ipynb),
      emit=json_emitter_factory(sys.stderr),
    ))
    loop.close()
    with tmp_fs.open(ipynb, 'r') as fr:
      shutil.copyfileobj(fr, sys.stdout)
