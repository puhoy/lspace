import os

import click

APP_NAME = 'elib'
CONFIG_FILE = 'config.yaml'

os.environ['FLASK_APP'] = 'elib/app.py'

app_dir = click.get_app_dir(APP_NAME)

