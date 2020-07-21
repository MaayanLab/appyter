import click
import requests

from appyter.remote.cli import remote

@remote.command(help='Inspect appyter for arguments (fields)')
@click.option('--output', envvar='OUTPUT', default='-', type=click.File('w'), help='The output location of the inspection json')
@click.argument('url', envvar='URL')
def nbinspect(url, output):
  response = requests.get(url, headers={'Accept': 'application/json'})
  assert response.status_code <= 299, f"Error ({response.status_code}): {response.text}"
  json.dump(response.json(), output)
