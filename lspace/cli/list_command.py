import os

import click

from lspace.cli import cli
from lspace.helpers import query_db
from flask import current_app


@cli.command(name='list', help='query your database')
@click.argument('query', nargs=-1)
@click.option('--path', is_flag=True)
@click.option('--details', is_flag=True)
def _list(query, path, details):
    results = query_db(query)

    if path:
        for result in results:
            click.echo(f'{os.path.join(current_app.config["LIBRARY_PATH"], result.path)}')
        return

    if details:
        for result in results:
            authors_str = ', '.join([author.name for author in result.authors])
            click.echo(f'{authors_str} - {result.title}')
            click.echo(f'{result.full_path}')
            click.echo(f'language: {result.language}')
            click.echo(f'year: {result.year}')
            click.echo(f'isbn: {result.isbn13}')
            click.echo()
        return


    for result in results:
        authors_str = ', '.join([author.name for author in result.authors])
        click.echo(f'{authors_str} - {result.title}')


