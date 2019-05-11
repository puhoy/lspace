import os
import click

from . import cli
from ..helpers import query_db


@cli.command(help='remove books from library')
@click.argument('query', nargs=-1)
def remove(query):
    if not query:
        exit()
    results = query_db(query)
    
    for result in results:        
        authors_str = ', '.join([author.name for author in result.authors])
        click.echo('\n')
        click.echo(f'{authors_str} - {result.title}')
        click.echo(f'{result.full_path}')
        if click.confirm('delete this book from library?'):
            click.echo('deleting')



