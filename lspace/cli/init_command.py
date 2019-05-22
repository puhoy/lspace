import os

import click
import yaml


from lspace.helpers import get_default_config
from lspace.cli import cli


@cli.command(help='generate a new config')
def init():
    from flask import current_app

    app_dir = current_app.config['APP_DIR']
    config_path = current_app.config['CONFIG_PATH']

    os.makedirs(app_dir, exist_ok=True)

    if os.path.exists(config_path):
        click.prompt('config exists - override?',
                     default=False, confirmation_prompt=True)

    default_config = get_default_config()
    with open(config_path, 'w') as config:
        yaml.dump(default_config, config)
    click.echo('written config file to %s' % config_path)

    return config_path
