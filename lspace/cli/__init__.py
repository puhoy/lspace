import os

#from flask.cli import AppGroup
from flask import Blueprint

cli_bp = Blueprint('cli', __name__, cli_group=None)

from .import_command import import_command
from .init_command import init
from .list_command import _list
from .tools_command import tools
from .remove_command import remove
from .reimport_command import reimport
from .export_command import export
from .web_command import web
from .version_command import version

if os.environ.get('LSPACE_DEV', None) == '1':
    from .db_command import db
