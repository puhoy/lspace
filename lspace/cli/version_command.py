import click

from lspace import __version__
from lspace.cli import cli_bp


@cli_bp.cli.command(help='print the version')
def version():
    click.echo(__version__)
