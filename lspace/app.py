
from . import create_app

import os
from flask_migrate import upgrade

def upgrade_db_if_needed(app):
    with app.app_context():

        upgrade()


config_path = os.environ.get('LSPACE_CONFIG', False)

app = create_app(config_path=config_path)


upgrade_db_if_needed(app)

from lspace.cli import cli as cli_group
