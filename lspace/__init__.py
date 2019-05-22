__version__ = '0.1.8'

import os

APP_NAME = 'lspace'
os.environ['FLASK_APP'] = os.path.join(os.path.dirname(__file__), 'app.py')


import click
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from lspace.helpers.init_logging import init_logging


db = SQLAlchemy()
migrate = Migrate()
whooshee = Whooshee()
marshmallow = Marshmallow()


def create_app(config_path=None, app_dir=None):
    from .helpers import read_config

    app = Flask(__name__)

    if not app_dir:
        app_dir = click.get_app_dir(APP_NAME)
    app.config['APP_DIR'] = app_dir

    if not config_path:
        config_path = os.path.join(app.config['APP_DIR'], 'config.yaml')

    app.config['CONFIG_PATH'] = config_path
    app.config['USER_CONFIG'] = read_config(config_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['USER_CONFIG']['database_path']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WHOOSHEE_DIR'] = os.path.join(app.config['APP_DIR'], 'whoosh_index')

    app.config['LIBRARY_PATH'] = os.path.abspath(os.path.expanduser(app.config['USER_CONFIG']['library_path']))

    init_logging(app.config['USER_CONFIG'].get('loglevel', 'info'))
    migration_dir = os.path.join(os.path.dirname(__file__), 'migrations')

    db.init_app(app)
    migrate.init_app(app, db, directory=migration_dir)
    whooshee.init_app(app)
    marshmallow.init_app(app)

    return app
