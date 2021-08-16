''' This module enables you to turn your jupyter notebook into a jinja2 template-driven web application. Or just parse for other purposes.
'''
import os
from appyter.magic import init

__version__ = open(os.path.join(os.path.dirname(__file__), 'VERSION'), 'r').read().strip()
