import os
import logging
from .helpers import read_config

from flask import Flask
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, current, upgrade
from flask_whooshee import Whooshee

from lspace import APP_NAME
from lspace import CONFIG_FILE
from lspace import app_dir

config = read_config()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['database_path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSHEE_DIR'] = os.path.join(app_dir, 'whoosh_index')

whooshee = Whooshee(app)

db = SQLAlchemy(app)

MIGRATION_DIR=os.path.join(os.path.dirname(__file__), 'migrations')
migrate = Migrate(app, db, directory=MIGRATION_DIR)

cli_group = AppGroup('cli')

def upgrade_db_if_needed(app):
    with app.app_context():
        upgrade()
        
upgrade_db_if_needed(app)

# import after app is created
from lspace.models import *
from lspace.cli import *
