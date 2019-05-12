
__version__ = '0.0.2'

import os

import click

APP_NAME = 'lspace'
CONFIG_FILE = 'config.yaml'

os.environ['FLASK_APP'] = 'lspace/app.py'

app_dir = click.get_app_dir(APP_NAME)
