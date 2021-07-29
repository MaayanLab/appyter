import os
import re
import sys
import click
import shutil

from appyter.cli import cli
from appyter.ext.fs import Filesystem
from appyter.context import get_env_from_kwargs, get_jinja2_env
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.ext.click import click_argument_setenv
from appyter.render.nbinspect import render_nbtemplate_json_from_nbtemplate
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.nbexecute import nbexecute_async, json_emitter_factory

@cli.command(
  help='Construct and execute an appyter given arguments',
  context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
  ),
)
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
@click.argument('args', nargs=-1)
def cwl_runner(ipynb, args):
  # prepare cwd/ipynb
  cwd = os.path.realpath(os.path.dirname(ipynb))
  ipynb = os.path.basename(ipynb)
  # nbinspect
  env = get_jinja2_env(
    config=get_env_from_kwargs(cwd=cwd, ipynb=ipynb, mode='inspect'),
  )
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  fields = render_nbtemplate_json_from_nbtemplate(env, nbtemplate)
  # convert arguments into context
  kwargs = dict([
    re.match(r'^--([^=]+)=(.+)$', arg).groups()
    for arg in args
  ])
  context = {}
  for field in fields:
    if field['args']['name'] in kwargs or field['args'].get('required') == True:
      context[field['args']['name']] = kwargs[field['args']['name']]
      if field['field'] == 'FileField':
        context[field['args']['name']] = os.path.basename(context[field['args']['name']])
  # nbconstruct with context
  env = get_jinja2_env(
    config=get_env_from_kwargs(cwd=cwd, ipynb=ipynb, mode='construct'),
    context=context,
  )
  nb = render_nb_from_nbtemplate(env, nbtemplate)
  # prepare tmpfs with notebook & symlinks to files
  with Filesystem('tmpfs://') as tmp_fs:
    with tmp_fs.open(ipynb, 'w') as fw:
      nb_to_ipynb_io(nb, fw)
    for field in fields:
      if field['field'] == 'FileField' and field['args']['name'] in context:
        # TODO: integrate with ext.fs
        os.symlink(
          os.path.realpath(kwargs[field['args']['name']]),
          tmp_fs.path(context[field['args']['name']]),
        )
    # nbexecute in tmpfs
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(nbexecute_async(
      cwd=tmp_fs.path(),
      ipynb=ipynb,
      # status updates go to stderr
      emit=json_emitter_factory(sys.stderr),
    ))
    loop.close()
    with tmp_fs.open(ipynb, 'r') as fr:
      # write result to stdout
      shutil.copyfileobj(fr, sys.stdout)
