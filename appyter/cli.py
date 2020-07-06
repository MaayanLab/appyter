import click
from click_default_group import DefaultGroup

@click.group(cls=DefaultGroup, default='flask-app')
def cli():
  pass
