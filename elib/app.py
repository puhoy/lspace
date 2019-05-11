import os

from flask import Flask
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_whooshee import Whooshee

from . import APP_NAME
from . import CONFIG_FILE
from . import app_dir

from .helpers import read_config

config = read_config()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = config['database_path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['WHOOSHEE_DIR'] = os.path.join(app_dir, 'whoosh_index')

whooshee = Whooshee(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

cli_group = AppGroup('cli')


# import after app is created
from .models import *
from .cli import *
