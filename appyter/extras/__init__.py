''' In the future, these will be independent of the profiles, injecting whatever needs to be.
For now, they're branches in the profile code.
'''

from appyter.cli import cli

@cli.command(help='List the available extra feature flags')
def list_extras():
  print('hide-code    Hide code by default')
  print('toc          Add a sticky table of contents to the rendered notebook')
  print('toggle-code  Add a button for toggling code visibility')
  print('catalog-integration  Add various appyter-catalog-integrated specific features')
