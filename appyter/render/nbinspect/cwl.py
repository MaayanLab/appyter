import os
import sys

from appyter.util import dict_filter_none
from appyter.parse.nbtemplate import parse_fields_from_nbtemplate

def render_cwl_from_nbtemplate(env, nb, ipynb=None, cwd=None):
  ''' Render a cwl representing the relevant Fields throughout the notebook.
  '''
  fields = list(parse_fields_from_nbtemplate(env, nb, deep=True))
  return {
    'cwlVersion': 'v1.0',
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
