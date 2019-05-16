
__version__ = '0.1.1'

import os

import click

APP_NAME = 'lspace'
CONFIG_FILE = 'config.yaml'

os.environ['FLASK_APP'] = os.path.join(os.path.dirname(__file__), 'app.py')

app_dir = click.get_app_dir(APP_NAME)
