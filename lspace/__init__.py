__version__ = '__version__ = '0.4.6''

import os
os.environ['FLASK_APP'] = os.path.join(os.path.dirname(__file__), 'app.py')

import click
from flask.cli import FlaskGroup

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_whooshee import Whooshee
from sqlalchemy import MetaData


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

from lspace.helpers.create_app import create_app


@click.group(cls=FlaskGroup, create_app=create_app, add_default_commands=False)
def cli():
    pass

