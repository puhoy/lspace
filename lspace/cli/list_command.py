import click

from lspace.cli import cli
from lspace.helpers.query import query_db


@cli.command(name='list', help='query your database')
@click.argument('query', nargs=-1)
@click.option('--path', is_flag=True)
@click.option('--details', is_flag=True)
def _list(query, path, details):
    results = query_db(query)

    if path:
        for result in results:
            click.echo(
                result.full_path)
        return

    if details:
        for result in results:
            head = '{result.authors_names} - {result.title}'.format(result=result)
            if result.shelve:
                head += ' ({result.shelve.name})'.format(result=result)
            click.echo(head)

            click.echo('{result.full_path}'.format(result=result))
            click.echo('language: {result.language}'.format(result=result))
            click.echo('year: {result.year}'.format(result=result))
            click.echo('isbn: {result.isbn13}'.format(result=result))
            click.echo()
        return

    for result in results:
        click.echo('{result.authors_names} - {result.title}'.format(result=result))
