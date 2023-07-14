import flask

import logging
import os

import click
from flask import Flask

from flask_migrate import upgrade as db_upgrade

from .init_logging import init_logging
from . import read_config

from lspace import db, whooshee, migrate


APP_NAME = 'lspace'

logger = logging.getLogger(__name__)


__version__ = '0.4.5'

os.environ['FLASK_APP'] = os.path.join(os.path.dirname(__file__), 'app.py')




def create_app():
    app = Flask(__name__,
                static_url_path='/_static', template_folder='/_templates') # we need /static for the frontend blueprint

    app_dir = click.get_app_dir(APP_NAME)
    app.config['APP_DIR'] = app_dir

    config_path = os.environ.get('LSPACE_CONFIG', False)
    if not config_path:
        config_path = os.path.join(app.config['APP_DIR'], 'config.yaml')

    app.config['CONFIG_PATH'] = config_path
    app.config['USER_CONFIG'] = read_config(config_path, app_dir)
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['USER_CONFIG']['database_path']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WHOOSHEE_DIR'] = os.path.join(app.config['APP_DIR'], 'whoosh_index')

    app.config['USER_CONFIG']['library_path'] = os.path.abspath(
        os.path.expanduser(app.config['USER_CONFIG']['library_path']))

    init_logging(app.config['USER_CONFIG']['loglevel'])

    migration_dir = os.path.join(os.path.dirname(__file__), '../migrations')

    db.init_app(app)

    # fix migration for sqlite: https://github.com/miguelgrinberg/Flask-Migrate/issues/61#issuecomment-208131722
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True, directory=migration_dir)
        else:
            migrate.init_app(app, db, directory=migration_dir)
        db_upgrade()

        def url_for_self(**args):
            return flask.url_for(flask.request.endpoint, **{**flask.request.view_args, **flask.request.args, **args})

        app.jinja_env.globals['url_for_self'] = url_for_self

    whooshee.init_app(app)

    @app.after_request
    def add_gnu_tp_header(response):
        # www.gnuterrypratchett.com
        response.headers.add("X-Clacks-Overhead", "GNU Terry Pratchett")
        return response

    from lspace.cli import cli_bp
    app.register_blueprint(cli_bp)

    return app

