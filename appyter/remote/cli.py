import click

from appyter.cli import cli

@cli.group(help='Interact with a remote appyter')
def remote():
  pass
