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
            if result.is_external_path:
                if click.confirm(f'this file is not part of the library - should i try to delete the file at "{result.full_path}"?'):
                    os.unlink(result.full_path)
                    db.session.delete(result)
                    db.session.commit()
                else:
                    click.echo("deleting metadata only...")
                    db.session.delete(result)
                    db.session.commit()
            else:
                os.unlink(result.full_path)
                db.session.delete(result)
                db.session.commit()
