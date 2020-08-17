import json
import click
from appyter.orchestration.cli import orchestration

@orchestration.command(help='A job triggered by an orchestration dispatcher queue')
@click.argument('job', type=str)
def job(job):
  from appyter.orchestration.job.job import execute
  execute(json.loads(job))
