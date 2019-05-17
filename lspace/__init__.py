__version__ = '0.1.4'

import os

import click

APP_NAME = 'lspace'
CONFIG_FILE = 'config.yaml'
MIGRATION_DIR = os.path.join(os.path.dirname(__file__), 'migrations')

os.environ['FLASK_APP'] = os.path.join(os.path.dirname(__file__), 'app.py')

app_dir = click.get_app_dir(APP_NAME)
