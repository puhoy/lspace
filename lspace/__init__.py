__version__ = '0.2.0'

import logging
import os

APP_NAME = 'lspace'
os.environ['FLASK_APP'] = os.path.join(os.path.dirname(__file__), 'app.py')

import click
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from sqlalchemy import MetaData

from lspace.helpers.init_logging import init_logging

# fix migration for sqlite: https://github.com/miguelgrinberg/Flask-Migrate/issues/61#issuecomment-208131722
naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))

migrate = Migrate()
whooshee = Whooshee()
logger = logging.getLogger(__name__)


def create_app(config_path=None, app_dir=None):
    from .helpers import read_config

    app = Flask(__name__)

    if not app_dir:
        app_dir = click.get_app_dir(APP_NAME)
    app.config['APP_DIR'] = app_dir

    if not config_path:
        config_path = os.path.join(app.config['APP_DIR'], 'config.yaml')

    app.config['CONFIG_PATH'] = config_path
    app.config['USER_CONFIG'] = read_config(config_path, app_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['USER_CONFIG']['database_path']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WHOOSHEE_DIR'] = os.path.join(app.config['APP_DIR'], 'whoosh_index')

    app.config['USER_CONFIG']['library_path'] = os.path.abspath(
        os.path.expanduser(app.config['USER_CONFIG']['library_path']))

    init_logging(app.config['USER_CONFIG']['loglevel'])

    migration_dir = os.path.join(os.path.dirname(__file__), 'migrations')

    db.init_app(app)

    # fix migration for sqlite: https://github.com/miguelgrinberg/Flask-Migrate/issues/61#issuecomment-208131722
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True, directory=migration_dir)
        else:
            migrate.init_app(app, db, directory=migration_dir)

    whooshee.init_app(app)

    return app
