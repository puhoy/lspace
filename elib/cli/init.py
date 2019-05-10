import os

import click
import yaml

from .. import CONFIG_FILE
from ..helpers import get_default_config

from .. import app_dir
from . import cli


@cli.command()
def init():
    os.makedirs(app_dir, exist_ok=True)
    config_path = os.path.join(app_dir, CONFIG_FILE)
    if os.path.exists(config_path):
        click.prompt('config exists - override?',
                     default=False, confirmation_prompt=True)

    default_config = get_default_config()
    with open(config_path, 'w') as config:
        yaml.dump(default_config, config)
