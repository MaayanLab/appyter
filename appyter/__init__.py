''' This module enables you to turn your jupyter notebook into a jinja2 template-driven web application. Or just parse for other purposes.
'''
import os
from appyter.magic import init
from importlib.metadata import version

__version__ = version(__package__)
