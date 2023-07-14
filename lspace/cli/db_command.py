from . import cli_bp

from flask_migrate import init, migrate, upgrade


@cli_bp.cli.group()
def db():
    pass


@db.command(name='init')
def _init():
    init()


@db.command(name='migrate')
def _migrate():
    migrate()


@db.command(name='upgrade')
def _upgrade():
    upgrade()
