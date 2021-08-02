import os
import sys
import json
import click

from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.ext.fs import Filesystem
from appyter.parse.nb import nb_from_ipynb_io
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.render.nbinspect.cli import nbinspect

from appyter.util import dict_filter_none
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

def render_cwl_from_nbtemplate(env, nb, ipynb=None, cwd=None):
  ''' Render a cwl representing the relevant Fields throughout the notebook.
  '''
  fields = list(parse_fields_from_nbtemplate(env, nb, deep=True))
  return {
    'cwlVersion': 'v1.2',
    'class': 'CommandLineTool',
    #
    'baseCommand': [
      sys.executable, '-u',
      '-m', 'appyter',
      'cwl-runner',
      os.path.join(cwd, ipynb),
    ],
    'inputs': dict_filter_none({
      field.args['name']: field.to_cwl()
      for field in fields
    }),
    'stderr': 'stderr.jsonl',
    'stdout': 'stdout.ipynb',
    'outputs': {
      'status': {
        'type': 'File',
        'streamable': True,
        'label': 'Realtime updates',
        'outputBinding': {
          'glob': 'stderr.jsonl',
        },
      },
      'report': {
        'type': 'File',
        'streamable': True,
        # 'format': '',
        'label': 'A jupyter notebook',
        'outputBinding': {
          'glob': 'stdout.ipynb',
        },
      },
    },
    # TODO: extract from appyter.json/section
    'label': 'Appyter',
    'doc': 'Description',
    # TODO: s:author / s:contributor / s:codeRepository / s:license / s:keywords
    's:programmingLanguage': 'Python',
    '$namespaces': {
      's': 'https://schema.org',
    },
    '$schemas': ['https://schema.org/version/latest/schemaorg-current-http.rdf'],
  }


@nbinspect.command(help='Create CWL Tool definition for appyter')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def cwl(cwd, ipynb, output, **kwargs):
  cwd = os.path.realpath(cwd)
  env = get_jinja2_env(config=get_env(cwd=cwd, ipynb=ipynb, mode='inspect', **kwargs))
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  json.dump(render_cwl_from_nbtemplate(env, nbtemplate, cwd=cwd, ipynb=ipynb), output)
