import click

from lspace.cli.import_command import import_wizard
from lspace.cli import cli
from lspace import db
from lspace.helpers.query import query_db


@cli.command(help='reimport books in library')
@click.argument('query', nargs=-1)
def reimport(query):
    if not query:
        exit()
    results = query_db(query)
    
    for result in results:
        click.echo('\n')
        click.echo('{result.authors_names} - {result.title}'.format(result=result))
        click.echo('{result.full_path}'.format(result=result))
        if click.confirm('reimport this?'):
            # delete without commit to exclude this book from db check
            db.session.delete(result)
            new_result = import_wizard(result.full_path, skip_library_check=True, move=True)
            if new_result:
                new_result.save()
            else:
                click.secho('no new entry - keeping the old one!')
                db.session.rollback()
