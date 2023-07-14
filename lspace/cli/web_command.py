import os


import click
import gunicorn.app.base
from flask import current_app

from lspace.api_v1_blueprint import api_blueprint
from lspace.cli import cli_bp
from lspace.frontend_blueprint import frontend_blueprint


@cli_bp.cli.command(help='start a webserver')
@click.option('--port', default=5000)
@click.option('--host', default='0.0.0.0')
@click.option('--debug', default=False, is_flag=True)
def web(host, port, debug):
    current_app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    current_app.register_blueprint(frontend_blueprint, url_prefix='')

    # todo: flask_env removed in 2.3.0
    if (os.environ.get('LSPACE_DEV', None) == '1') or debug:
        os.environ['FLASK_ENV'] = 'development'
        print(os.environ['FLASK_ENV'])
        current_app.run(debug=True, host=host, port=port)
    else:
        options = {
            'bind': '{HOST}:{PORT}'.format(HOST=host, PORT=port)
        }
        StandaloneApplication(current_app, options).run()


# http://docs.gunicorn.org/en/latest/custom.html
class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in self.options.items()
                       if key in self.cfg.settings and value is not None])
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

