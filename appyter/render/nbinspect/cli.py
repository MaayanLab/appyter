from appyter.cli import cli
from click_default_group import DefaultGroup

@cli.group(cls=DefaultGroup, default='nbtemplate-json', help='Serialize various formats from appyter inspection')
def nbinspect():
  pass
