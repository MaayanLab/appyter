import os
import re
import sys
import click
import shutil
import fsspec
import tempfile
from pathlib import Path

from appyter.cli import cli
from appyter.ext.json import try_json_loads
from appyter.context import get_env_from_kwargs, get_jinja2_env
from appyter.ext.urllib import join_slash
from appyter.parse.nb import nb_from_ipynb_io, nb_to_ipynb_io
from appyter.ext.click import click_argument_setenv
from appyter.render.nbinspect.nbtemplate_json import render_nbtemplate_json_from_nbtemplate
from appyter.render.nbconstruct import render_nb_from_nbtemplate
from appyter.render.nbexecute import nbexecute_async, json_emitter_factory

def parse_cli(arg):
  m = re.match(r'^--([^=]+)(=(.*))?$', arg)
  if m and m.group(2) is not None:
    return (m.group(1), try_json_loads(m.group(3)))
  else:
    return (m.group(1), True)

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
  with fsspec.open(join_slash(cwd, ipynb), 'r') as fr:
    nbtemplate = nb_from_ipynb_io(fr)
  fields = render_nbtemplate_json_from_nbtemplate(env, nbtemplate)
  # convert arguments into context
  kwargs = dict(map(parse_cli, args))
  context = {}
  for field in fields:
    if field['field'] == 'BoolField' and field['args']['name'] not in kwargs:
      kwargs[field['args']['name']] = False
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
  # prepare temporary directory with notebook
  tmp_fs = Path(tempfile.mkdtemp())
  with (tmp_fs/ipynb).open('w') as fw:
    nb_to_ipynb_io(nb, fw)
  # nbexecute in temporary directory
  import asyncio
  loop = asyncio.get_event_loop()
  loop.run_until_complete(nbexecute_async(
    cwd=str(tmp_fs),
    ipynb=ipynb,
    # status updates go to stderr
    emit=json_emitter_factory(sys.stderr),
  ))
  loop.close()
  with (tmp_fs/ipynb).open('r') as fr:
    # write result to stdout
    shutil.copyfileobj(fr, sys.stdout)
  # cleanup temporary directory
  shutil.rmtree(tmp_fs)
