import os
import click

from lspace.cli import cli
from lspace.helpers.query import query_db
from lspace import db


@cli.command(help='remove books from library')
@click.argument('query', nargs=-1)
def remove(query):
    if not query:
        exit()
    results = query_db(query)
    
    for result in results:        
        click.echo('\n')
        click.echo('{result.authors_names} - {result.title}'.format(result=result))
        click.echo('{result.full_path}'.format(result=result))
        if click.confirm('delete this book from library?'):
            os.unlink(result.full_path)
            db.session.delete(result)
            db.session.commit()
