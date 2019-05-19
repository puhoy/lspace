from flask_migrate import upgrade

from . import create_app


def upgrade_db_if_needed(app):
    with app.app_context():
        upgrade()


app = create_app()
upgrade_db_if_needed(app)

from lspace.cli import cli as cli_group
