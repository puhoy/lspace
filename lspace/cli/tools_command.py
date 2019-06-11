import click
import isbnlib
import yaml

from lspace import db
from lspace import whooshee
from lspace.cli import cli
from lspace.cli.import_command import _copy_to_library
from lspace.file_types import get_file_type_class
from lspace.models import Book
from lspace.models.meta_cache import MetaCache
import logging

logger = logging.getLogger(__name__)

@cli.group(help='tools you probably never need... :P')
def tools():
    pass


@tools.command(help='update paths after changing file_format setting in config')
def update_paths():
    books = Book.query.all()
    for book in books:
        print(book.path)
        try:
            source_path = book.full_path
            source_in_library = book.path
            FileClass = get_file_type_class(source_path)
            file_type_object = FileClass(source_path)
            new_path = _copy_to_library(file_type_object, book, True)
            book.path = new_path
            book.save()
            click.echo('moved {source} to {new_path}'.format(source=source_in_library, new_path=new_path))
        except Exception as e:
            logger.exception('error moving file', exc_info=True)

@tools.command(help='convert isbn-10 to isbn-13')
@click.argument('dirtyisbn')
def convert_to_isbn13(dirtyisbn):
    click.echo(isbnlib.to_isbn13(dirtyisbn))


@tools.command(help='find metadata for books by words')
@click.argument('words')
def find_meta_by_text(words):
    if isbnlib.is_isbn13:
        click.echo('%s looks like isbn!' % words)
        results = isbnlib.meta(words, service='openl')
    else:
        results = isbnlib.goom(words)
    click.echo(yaml.dump(results))


@tools.command(help='rebuild the search index for your library')
def rebuild_search_index():
    whooshee.reindex()


@tools.command(help='clear metadata cache')
def clear_cache():
    num = MetaCache.query.delete()
    db.session.commit()
    click.echo('deleted %s rows' % num)

@tools.command(help='start ipython')
def shell():
    import rlcompleter
    import pdb
    import rlcompleter, readline
    readline.parse_and_bind('tab: complete')

    pdb.Pdb.complete = rlcompleter.Completer(locals()).complete

    breakpoint()