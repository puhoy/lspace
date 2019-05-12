import click

from lspace import __version__
from . import cli


@cli.command(help='print the version')
def version():
    click.echo(__version__)
