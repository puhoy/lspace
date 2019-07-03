import os

import click

from lspace.app import app
from lspace.cli import cli
from lspace.api_v1_blueprint import api_blueprint


@cli.command(help='start a webserver')
@click.option('--port', default=5000)
@click.option('--host', default='0.0.0.0')
def web(host, port):
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    kwargs = dict(
        host=host,
        port=port
    )

    if os.environ.get('LSPACE_DEV', None) == '1':
        app.run(debug=True, **kwargs)
    else:
        app.run(**kwargs)
