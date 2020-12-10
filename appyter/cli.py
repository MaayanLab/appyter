import click
from appyter import __version__
from click_default_group import DefaultGroup

@click.group(cls=DefaultGroup, default='flask-app')
@click.version_option(
  prog_name='appyter',
  version=__version__,
)
def cli():
  pass
