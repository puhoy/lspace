import logging
from pathlib import PurePath, Path
from urllib.parse import urlparse

import click
import yaml
from typing import List
from typing import Union

from lspace.cli.import_command.add_book_to_db import add_book_to_db
from lspace.cli.import_command.add_to_shelf import add_to_shelf
from lspace.cli.import_command.check_if_in_library import check_if_in_library
from lspace.cli.import_command.copy_to_library import copy_to_library
from lspace.cli.import_command.import_from_api import ApiImporter
from lspace.cli.import_command.import_from_calibre import CalibreWrapper
from lspace.cli.import_command.import_options._options import other_choices
from lspace.file_types import FileTypeBase
from lspace.file_types import get_file_type_object
from lspace.models import Book

logger = logging.getLogger(__name__)


def bold(s):
    return click.style(s, bold=True)


def is_calibre_library(path):
    if PurePath(path).suffix == '.db':
        c = CalibreWrapper(path)
        library_id = None
        try:
            library_id = c.get_library_id()
        except Exception as e:
            logger.exception('', exc_info=True)
            pass

        if library_id:
            return True

    return False


def is_api(url):
    parsed = urlparse(url)
    scheme = parsed.scheme
    path = parsed.path

    clean_api_path = '/api/v1/'
    if (scheme in ['http', 'https']) and (clean_api_path in path):
        # todo: fetch /version ?
        return True

    return False


def import_wizard(path, skip_library_check, move, inplace):
    # type: (str, bool, bool, bool) -> Union[Book, None]
    click.echo(bold('importing ') + path)

    if is_calibre_library(path):
        if click.confirm('this looks like a calibre library - import?', default=True):
            calibre_importer = CalibreWrapper(path)
            for book_path, book in calibre_importer.import_books():
                import_file_wizard(book_path, skip_library_check, move, inplace, metadata=[book])
            return

    if is_api(path):
        if click.confirm('this looks like the lspace api - import?', default=True):
            api_importer = ApiImporter(path)
            for book_path, book in api_importer.start_import(skip_library_check=skip_library_check):
                import_file_wizard(book_path, skip_library_check, move=False, inplace=False, metadata=[book])
        return

    return import_file_wizard(path, skip_library_check, move, inplace)


def import_file_wizard(path, skip_library_check, move, inplace, metadata=None):
    # type: (str, bool, bool, bool, List[Book]) -> Union[Book, None]

    abspath = Path(path).resolve()
    if not abspath.exists():
        logger.error(f"cannot find file at {abspath}, skipping")
        return

    try:
        file_type_object = get_file_type_object(abspath)
    except Exception as e:
        logger.exception('error reading {path}'.format(path=abspath), exc_info=True)
        click.secho('error reading {path}'.format(path=abspath), fg='red')
        return

    if not file_type_object:
        # skip, because we have no class to read this file
        click.echo('skipping %s' % path)
        return

    if not skip_library_check and Book.query.filter_by(md5sum=file_type_object.get_md5()).first():
        click.echo(bold('already imported') + ', skipping ' + path)
        return

    if not metadata:
        isbns_with_metadata = file_type_object.fetch_results()
    else:
        isbns_with_metadata = metadata

    if len(isbns_with_metadata) == 0:
        click.echo('could not find any isbn or metadata for %s' % file_type_object.filename)
        choice = choose_result(file_type_object, [])

    else:
        choice = choose_result(file_type_object, isbns_with_metadata)

    logger.debug('choice was %s' % choice)

    while choice in list(other_choices.keys()):
        # if choice is one of "other choices", its not one of the results,
        # but one of the strings mapped to functions

        function_that_gets_new_choices = other_choices.get(choice)['function']
        isbns_with_metadata = function_that_gets_new_choices(
            file_type_object=file_type_object,
            old_choices=isbns_with_metadata,
        )

        if isbns_with_metadata is not False:
            choice = choose_result(file_type_object, isbns_with_metadata)
        else:
            # "skip" is the only function that returns false here
            choice = False

    if choice:
        book = _import(file_type_object, choice, move, inplace)
        return book
    else:
        click.echo('skipping %s' % file_type_object.filename, color='yellow')


def choose_result(file_type_object, isbns_with_metadata):
    # type: (FileTypeBase, [Book]) -> Book
    if not isbns_with_metadata:
        click.secho('no results found :(', fg='yellow')

    formatted_choices = format_metadata_choices(
        isbns_with_metadata)

    click.echo(''.join(formatted_choices.values()))

    choices = list(formatted_choices.keys())

    if len(isbns_with_metadata) >= 1:
        default = '1'
    else:
        default = 's'

    ret = click.prompt('choose result for ' +
                       click.style('{filename}'.format(filename=file_type_object.filename), bold=True),
                       type=click.Choice(choices),
                       default=default)
    if ret in list(other_choices.keys()):
        choice = ret
    else:
        try:
            idx = int(ret) - 1
            choice = isbns_with_metadata[idx]
        except Exception as e:
            logger.exception('cant convert %s to int!' % ret, exc_info=True)
            return False

    return choice


def format_metadata_choices(isbns_with_metadata):
    # type: ([Book]) -> dict

    formatted_metadata = {
        # 'choice': 'str shown to user'
    }
    for idx, meta in reversed(list(enumerate(isbns_with_metadata))):
        logger.info('adding %s' % meta)

        formatted_metadata[str(idx + 1)] = click.style(
            '{index}: {head}\n'.format(index=idx + 1, head=meta.formatted_output_head()),
            bold=True)
        formatted_metadata[str(idx + 1)] += meta.formatted_output_details() + '\n'

    for key, val in other_choices.items():
        formatted_metadata[key] = \
            click.style(yaml.dump({
                key: val['explanation']},
                allow_unicode=True), bold=True)

    logger.debug('formatted data is %s' % formatted_metadata)
    return formatted_metadata


def similar_books_decide_import(book_choice):
    similar_books = check_if_in_library(book_choice)
    if similar_books:
        click.echo(bold('found similar books in library:'))
        for book in similar_books:
            click.echo(bold('{book.authors_names} - {book.title}'.format(book=book)))
            click.echo('isbn: {book.isbn13}'.format(book=book))
            click.echo('{book.path}\n'.format(book=book))

        if not click.confirm('import anyway?'):
            return False

    return True


def _import(file_type_object, book_choice, move_file, inplace):
    # type: (FileTypeBase, Book, bool, bool) -> Union[Book, None]
    logger.debug('importing %s, %s' % (file_type_object, book_choice))
    logger.debug(file_type_object)

    book_choice.path = file_type_object.path

    do_import = similar_books_decide_import(book_choice)
    if not do_import:
        click.echo(bold('skipping {path}'.format(path=file_type_object.path)))
        return

    add_to_shelf(book_choice)

    if inplace:
        book = add_book_to_db(file_type_object, book_choice, file_type_object.path, is_external_path=True)

    else:
        path_in_library = copy_to_library(file_type_object.path, book_choice, move_file)
        if path_in_library:
            book = add_book_to_db(file_type_object, book_choice, path_in_library, is_external_path=False)
        else:
            click.secho('could not import %s' % file_type_object.path, fg='red')
            return None

    click.secho('imported %s - %s' % (book.authors_names, book.title), fg='green')
    return book
