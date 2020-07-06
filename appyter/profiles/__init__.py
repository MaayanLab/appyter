''' ```eval_rst
Each submodule represents a profile extending from :mod:`appyter.profiles.default` which provide different rendering themes.
``` '''

from appyter.cli import cli
@cli.command(help='List the available profiles available with the profile option')
def list_profiles():
  # TODO: introspect to get this
  print('default    Bare profile with no styling')
  print('bootstrap  Base bootstrap styles on vanilla forms')
  print('biojupies  Biojupies style bootstrap form elements')
