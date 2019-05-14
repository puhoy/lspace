import os
import click
import shutil

from lspace.cli.import_command import guided_import
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
            new_result = guided_import(result.full_path, skip_library_check=True, move=True)
            if new_result:
                db.session.delete(result)
                db.session.commit()
            else:
                click.secho('no new entry - keeping the old one!')
