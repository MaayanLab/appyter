import click
import yaml
from appyter import __version__
import logging.config as loggingConf
from click_default_group import DefaultGroup
from appyter.ext.click import click_option_setenv
from appyter.ext.dict import dict_merge

@click.group(cls=DefaultGroup, default='flask-app')
@click.version_option(
  prog_name='appyter',
  version=__version__,
)
@click_option_setenv('--debug', envvar='APPYTER_DEBUG', default=True, help='Debug or production')
@click_option_setenv('--logging', envvar='APPYTER_LOGGING', default='{}', help='Appyter logging config and/or file')
def cli(logging=None, debug=False):
  loggingConf.dictConfig(dict_merge({
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
      'standard': {
        'format': '%(levelname)s:%(name)s: %(message)s',
      },
    },
    'handlers': {
      'console': {
        'level': 'DEBUG' if debug else 'INFO',
        'formatter': 'standard',
        'class': 'logging.StreamHandler',
        'stream': 'ext://sys.stderr',
      },
    },
    'loggers': {
      '': {
        'handlers': ['console'],
        'level': 'INFO',
        'propagate': False,
      },
      __package__: {
        'handlers': ['console'],
        'level': 'DEBUG',
        'propagate': False,
      },
    },
  }, **yaml.safe_load(logging)))
