''' ```eval_rst
Each submodule represents a profile extending from :mod:`appyter.profiles.default` which provide different rendering themes.
``` '''

import os
from appyter.cli import cli
from appyter.ext.importlib import importdir

# capture all profiles in the directory and add to profiles/globals
profiles = {}
importdir(os.path.dirname(__file__), __package__, profiles)
globals().update(**profiles)

# register list_profiles command based on profile names and first line of module docstring
@cli.command(help='List the available profiles for the profile option')
def list_profiles():
  profile_name_max_size = max(map(len, profiles.keys()))
  for profile, mod in profiles.items():
    doc_first_line = mod.__doc__.strip().splitlines()[0].strip()
    print(profile.ljust(profile_name_max_size+1), doc_first_line)
