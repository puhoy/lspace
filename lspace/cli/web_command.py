import os

import click

from lspace.app import app
from lspace.cli import cli


@cli.command(help='start a webserver')
@click.option('--port', default=5000)
@click.option('--host', default='0.0.0.0')
def web(host, port):
    from lspace.api_blueprint import api_blueprint
    app.register_blueprint(api_blueprint)

    kwargs = dict(
        host=host,
        port=port
    )

    if os.environ.get('LSPACE_DEV', None) == '1':
        app.run(debug=True, **kwargs)
    else:
        app.run(**kwargs)
