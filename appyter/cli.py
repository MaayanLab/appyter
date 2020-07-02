import click

@click.group()
def cli():
  pass

@cli.command(help='List the available profiles')
def list_profiles():
  # todo introspect to get this
  print('default    Bare profile with no styling')
  print('bootstrap  Base bootstrap styles on vanilla forms')
  print('biojupies  Biojupies style bootstrap form elements')
