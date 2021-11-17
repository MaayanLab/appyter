import os
import sys
import json
import click

from appyter import __version__
from appyter.context import get_env, get_jinja2_env
from appyter.ext.click import click_option_setenv, click_argument_setenv
from appyter.ext.fs import Filesystem
from appyter.parse.nb import nb_from_ipynb_io
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate
from appyter.render.nbinspect.cli import nbinspect

from appyter.util import dict_filter_none
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

def render_cwl_from_nbtemplate(env, nb, ipynb=None, cwd=None, info=None):
  ''' Render a cwl representing the relevant Fields throughout the notebook.
  '''
  fields = list(parse_fields_from_nbtemplate(env, nb, deep=True))
  schema = {
    'cwlVersion': 'v1.2',
    'class': 'CommandLineTool',
  }
  # potentially extract info from appyter embedded metadata if not provided
  if info is None and 'appyter' in nb.metadata and 'info' in nb.metadata['appyter']:
    info = nb.metadata['appyter']['info']
  if info is not None:
    schema.update({
      'baseCommand': [
        'python3', '-u',
        '-m', 'appyter',
        'cwl-runner',
        f"/app/{ipynb}",
      ],
      "hints": [
        {
          "class": "DockerRequirement",
          "dockerPull": f"maayanlab/appyter-{info['name'].lower()}:{info['version']}:{info['version']}-{__version__}"
        }
      ],
      "label": info['title'],
      "doc": info['description'],
      "s:author": ', '.join(author['name'] for author in info['authors']),
      "s:license": info['license'],
      "s:codeRepository": info['url'],
      "s:keywords": info['tags'],
    })
  else:
    schema.update({
      'baseCommand': [
        sys.executable, '-u',
        '-m', 'appyter',
        'cwl-runner',
        os.path.join(cwd, ipynb),
      ],
    })
  #
  schema.update({
    'inputs': list(dict_filter_none({
      field.args['name']: field.to_cwl()
      for field in fields
    }).values()),
    'stderr': 'stderr.jsonl',
    'stdout': ipynb,
    'outputs': [
      {
        'id': 'status',
        'type': 'File',
        'streamable': True,
        'label': 'Realtime updates',
        'outputBinding': {
          'glob': 'stderr.jsonl',
        },
      },
      {
        'id': 'report',
        'type': 'File',
        'streamable': True,
        # 'format': '',
        'label': 'A jupyter notebook',
        'outputBinding': {
          'glob': ipynb,
        },
      },
    ],
    's:programmingLanguage': 'Python',
    '$namespaces': {
      's': 'https://schema.org',
    },
    '$schemas': ['https://schema.org/version/latest/schemaorg-current-http.rdf'],
  })
  return schema


@nbinspect.command(help='Create CWL Tool definition for appyter')
@click.option('-o', '--output', default='-', type=click.File('w'), help='The output location of the inspection json')
@click.option('-i', '--info', default=None, type=click.File('r'), help='An appyter.json file for extra metadata as described in https://github.com/MaayanLab/appyter-catalog/blob/master/schema/appyter-validator.json')
@click_option_setenv('--cwd', envvar='APPYTER_CWD', default=os.getcwd(), help='The directory to treat as the current working directory for templates and execution')
@click_argument_setenv('ipynb', envvar='APPYTER_IPYNB')
def cwl(cwd, ipynb, info, output, **kwargs):
  cwd = os.path.realpath(cwd)
  env = get_jinja2_env(config=get_env(cwd=cwd, ipynb=ipynb, mode='inspect', **kwargs))
  nbtemplate = nb_from_ipynb_io(Filesystem(cwd).open(ipynb, 'r'))
  info = json.load(info) if info is not None else None
  json.dump(render_cwl_from_nbtemplate(env, nbtemplate, cwd=cwd, ipynb=ipynb, info=info), output)