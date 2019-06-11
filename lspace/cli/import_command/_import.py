import logging

import click
import yaml

from lspace.cli.import_command.add_book_to_db import add_book_to_db
from lspace.cli.import_command.check_if_in_library import check_if_in_library
from lspace.cli.import_command.copy_to_library import _copy_to_library
from lspace.cli.import_command.options import other_choices
from lspace.file_types import get_file_type_object
from lspace.models import Book

logger = logging.getLogger(__name__)


def bold(s):
    return click.style(s, bold=True)


def import_wizard(path, skip_library_check, move):
    click.echo(bold('importing ') + path)

    try:
        f = get_file_type_object(path)
    except Exception as e:
        logger.exception('error reading {path}'.format(path=path), exc_info=True)
        click.secho('error reading {path}'.format(path=path), fg='red')
        return

    if f:
        if not skip_library_check and Book.query.filter_by(md5sum=f.get_md5()).first():
            click.echo(bold('already imported') + ', skipping...')
            return

        isbns_with_metadata = f.fetch_results()

        if len(isbns_with_metadata) == 0:
            click.echo('could not find any isbn or metadata for %s' % f.filename)
            choice = choose_result(f, [])

        else:
            choice = choose_result(f, isbns_with_metadata)

        logger.debug('choice was %s' % choice)

        while choice in list(other_choices.keys()):
            # if choice is one of "other choices", its not one of the results,
            # but one of the strings mapped to functions

            function_that_gets_new_choices = other_choices.get(choice)['function']
            isbns_with_metadata = function_that_gets_new_choices(file_type_object=f,
                                                                 old_choices=isbns_with_metadata,
                                                                 )

            if isbns_with_metadata is not False:
                choice = choose_result(f, isbns_with_metadata)
            else:
                # "skip" is the only function that returns false here
                choice = False

        if choice:
            return _import(f, choice, move)
        else:
            click.echo('skipping %s' % path, color='yellow')

    else:
        # skip, because we have no class to read this file
        click.echo('skipping %s' % path)


def choose_result(file_type_object, isbns_with_metadata):
    if not isbns_with_metadata:
        click.secho('no results found :(', fg='yellow')

    formatted_choices = format_metadata_choices(
        isbns_with_metadata)

    click.echo(''.join(formatted_choices.values()))

    choices = list(formatted_choices.keys())

    ret = click.prompt('choose result for %s' % file_type_object.filename,
                       type=click.Choice(choices))
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
    # type: (Book) -> dict

    formatted_metadata = {
        # 'choice': 'str shown to user'
    }
    for idx, meta in enumerate(isbns_with_metadata):
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


def _import(file_type_object, choice, move_file):
    logger.debug('importing %s, %s' % (file_type_object, choice))
    logger.debug(file_type_object)

    similar_books = check_if_in_library(choice)
    if similar_books:
        click.echo(bold('found similar books in library:'))
        for book in similar_books:
            click.echo(bold('{book.authors_names} - {book.title}'.format(book=book)))
            click.echo('isbn: {book.isbn13}'.format(book=book))
            click.echo('{book.path}\n'.format(book=book))
        if not click.confirm('import anyway?'):
            click.echo(bold('skipping %s' % file_type_object.path))
            return

    path_in_library = _copy_to_library(file_type_object, choice, move_file)
    if path_in_library:
        book = add_book_to_db(file_type_object, choice, path_in_library)
        click.secho('imported %s - %s' % (book.authors_names, book.title), fg='green')
        return book
    else:
        click.secho('could not import %s' % file_type_object.path, fg='red')
