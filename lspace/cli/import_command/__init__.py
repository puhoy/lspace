import copy
import logging
from typing import Union

import click
import yaml

from lspace.cli.import_command._import import guided_import
from lspace.cli.import_command.add_book_to_db import add_book_to_db
from lspace.cli.import_command.copy_to_library import _copy_to_library
from lspace.cli.import_command.lookup_isbn import lookup_isbn
from lspace.cli.import_command.skip_book import skip_book
from lspace.cli.import_command.run_search import run_search as _run_search

from lspace.file_types import get_file_type_class

from lspace.models.book import Book
from .. import cli

logger = logging.getLogger(__name__)


@cli.command(name='import', help='import ebooks into your database')
@click.argument('document_path', type=click.Path(exists=True), nargs=-1)
@click.option('--skip-library-check', help='dont check if this file is in the library already', default=False, is_flag=True)
@click.option('--move', help='move imported files instead copying', default=False, is_flag=True)
def import_command(document_path, skip_library_check, move):
    for path in document_path:
        guided_import(path, skip_library_check, move)
