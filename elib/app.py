
import logging
import os
from shutil import copyfile, move

import click
import isbnlib
import yaml

from flask import Flask
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy
from pick import pick
from slugify import slugify
from flask_migrate import Migrate


from . import APP_NAME
from . import CONFIG_FILE

from .helpers import read_config

config = read_config()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config['database_path']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)


cli_group = AppGroup('cli')

from .file_types import get_file_type_class
from .models.author import Author
from .models.book import Book
from .models.book_author_association import book_author_association_table

from .cli import *