from appyter.cli import cli
from click_default_group import DefaultGroup

@cli.group(cls=DefaultGroup, default='dispatcher', help='Helpers for orchestrating appyters using different runtimes')
def orchestration():
  pass
