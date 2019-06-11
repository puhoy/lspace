import logging

import click

from lspace.cli.import_command import _copy_to_library
from lspace.cli.tools_command import tools
from lspace.file_types import get_file_type_object
from lspace.models import Book

logger = logging.getLogger(__name__)


def update_path(book):
    source_path = book.full_path

    file_type_object = get_file_type_object(source_path)

    new_path = _copy_to_library(file_type_object, book, True)

    book.path = new_path
    book.save()

    return new_path


@tools.command(help='update paths after changing file_format setting in config')
def _update_paths():
    books = Book.query.all()
    for book in books:

        source_in_library = book.path
        new_path = update_path(book)

        try:
            click.echo('moved {source} to {new_path}'.format(source=source_in_library, new_path=new_path))
        except Exception as e:
            logger.exception('error moving file', exc_info=True)