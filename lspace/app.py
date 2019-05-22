import os
from flask_migrate import upgrade

from lspace import init_logging
from . import create_app


def upgrade_db_if_needed(app):
    with app.app_context():
        upgrade()


config_path = os.environ.get('LSPACE_CONFIG', False)

app = create_app(config_path=config_path)
init_logging()

upgrade_db_if_needed(app)

from lspace.cli import cli as cli_group
