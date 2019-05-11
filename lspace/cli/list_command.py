import os
import click

from ..models import Author, Book
from . import cli
from ..config import user_config, library_path


@cli.command(name='list')
@click.argument('query', nargs=-1)
@click.option('--path', is_flag=True)
def _list(query, path):
    if not query:
        results = Book.query.all()
    else:
        results = Book.query.whooshee_search(' '.join(query)).all()
    if path:
        for result in results:
            
            print(f'{os.path.join(library_path, result.path)}')
        return


    for result in results:
        authors_str = ', '.join([author.name for author in result.authors])
        print(f'{authors_str} - {result.title}')

