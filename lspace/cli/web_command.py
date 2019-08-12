import os

import click

from lspace.app import app
from lspace.cli import cli
from lspace.api_v1_blueprint import api_blueprint
from lspace.frontend_blueprint import frontend_blueprint

from gunicorn.arbiter import Arbiter
from gunicorn.config import Config


@cli.command(help='start a webserver')
@click.option('--port', default=5000)
@click.option('--host', default='0.0.0.0')
@click.option('--debug', default=False, is_flag=True)
def web(host, port, debug):
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    app.register_blueprint(frontend_blueprint, url_prefix='')

    app.secret_key = os.urandom(30)

    if (os.environ.get('LSPACE_DEV', None) == '1') or debug:
        os.environ['FLASK_ENV'] = 'development'
        print(os.environ['FLASK_ENV'])
        app.run(debug=True, host=host, port=port)
    else:
        from gunicorn.app.base import Application

        class FlaskApplication(Application):
            def init(self, parser, opts, args):
                return {
                    'bind': '{0}:{1}'.format(host, port),
                    'workers': 4
                }

            def load(self):
                return app

        FlaskApplication().run()

        arbiter = Arbiter(app)
        arbiter.run()
