import os

from flask.cli import AppGroup

cli = AppGroup('cli')

from .import_command import import_command
from .init_command import init
from .list_command import _list
from .tools_command import tools
from .remove_command import remove
from .reimport_command import reimport
from .export_command import export
from .version_command import version

print(os.environ.get('LSPACE_DEV', None))
if os.environ.get('LSPACE_DEV', None) == '1':
    from .db_command import db
