import os
import click
import shutil

from lspace.cli.import_command import import_wizard
from . import cli
from ..helpers import query_db
from ..app import db


@cli.command(help='reimport books in library')
@click.argument('query', nargs=-1)
def reimport(query):
    if not query:
        exit()
    results = query_db(query)
    
    for result in results:        
        authors_str = ', '.join([author.name for author in result.authors])
        click.echo('\n')
        click.echo(f'{authors_str} - {result.title}')
        click.echo(f'{result.full_path}')
        if click.confirm('reimport this?'):
            # delete without commit to exclude this book from db check
            db.session.delete(result)
            new_result = import_wizard(result.full_path, skip_library_check=True, move=True)
            if new_result:
                db.session.commit()
            else:
                click.secho('no new entry - keeping the old one!')
                db.session.rollback()
