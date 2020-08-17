''' Orchestration dispatcher implementations using different backends
'''

import os
from appyter.util import importdir
from appyter.orchestration.cli import orchestration

# capture all dispatchers in the directory and add to dispatchers/globals
dispatchers = {}
importdir(os.path.dirname(__file__), __package__, dispatchers)
globals().update(**dispatchers)

@orchestration.command(help='List the dispatchers currently available')
def list_dispatchers():
  dispatcher_name_max_size = max(map(len, dispatchers.keys()))
  for dispatcher, mod in dispatchers.items():
    doc_first_line = mod.__doc__.strip().splitlines()[0].strip()
    print(dispatcher.ljust(dispatcher_name_max_size+1), doc_first_line)
