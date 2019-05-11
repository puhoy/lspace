
import click

from ..models import Author, Book
from . import cli


@cli.command(name='list')
@click.argument('query', nargs=-1)
def _list(query):
    pass
