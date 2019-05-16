import copy
import logging

import click
import yaml
from lspace.cli.import_command.add_book_to_db import add_book_to_db
from lspace.cli.import_command.copy_to_library import _copy_to_library
from lspace.cli.import_command.lookup_isbn import lookup_isbn
from lspace.cli.import_command.skip_book import skip_book
from lspace.cli.import_command.run_search import run_search as _run_search

from lspace.file_types import get_file_type_class
from lspace.models import Book

logger = logging.getLogger(__name__)

run_search = 'run another query'
isbn_lookup = 'lookup by isbn'
# specify_manually = 'specify manually'
skip = 'skip'

other_choices = {
    'q': dict(
        function=_run_search,
        explanation=run_search),
    'i': dict(
        function=lookup_isbn,
        explanation=isbn_lookup),
    's': dict(
        function=skip_book,
        explanation=skip)
}


def guided_import(path, skip_library_check, move):
    click.echo('processing %s' % path)
    FileClass = get_file_type_class(path)
    if FileClass:
        try:
            f = FileClass(path)
        except Exception as e:
            logger.error("error reading %s" % path, exc_info=True)
            click.secho("error reading %s" % path, fg='red')
            return

        if not skip_library_check and Book.query.filter_by(md5sum=f.get_md5()).first():
            click.echo('%s already imported, skipping...' % path)
            return

        click.echo('getting metadata for %s' % path)

        isbns_with_metadata = f.find_metadata()

        if len(isbns_with_metadata) == 0:
            click.echo('could not find any isbn or metadata for %s' % f.filename)
            choice = choose_result(f, [])

        elif len(isbns_with_metadata) == 1:
            click.echo('got one result: %s - importing!' % isbns_with_metadata[0])
            choice = isbns_with_metadata[0]

        else:
            choice = choose_result(f, isbns_with_metadata)

        logging.debug('choice was %s' % choice)

        while choice in list(other_choices.keys()):
            # if choice is one of "other choices", its not one of the results,
            # but one of the strings mapped to functions

            function_that_gets_new_choices = other_choices.get(choice)['function']
            new_results = function_that_gets_new_choices()

            if new_results is not False:
                choice = choose_result(f, new_results)
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


def format_metadata_choices(isbns_with_metadata) -> dict:
    isbns_with_metadata = copy.deepcopy(isbns_with_metadata)

    formatted_metadata = {
        # 'choice': 'str shown to user'
    }
    for idx, meta in enumerate(isbns_with_metadata):
        logger.info('adding %s' % meta)

        authors = ', '.join([author for author in meta.pop('Authors', [])])
        title = meta.pop('Title')
        formatted_metadata[str(idx + 1)] = \
            f'\n{idx + 1}: {authors} - {title}\n' + yaml.dump(meta, allow_unicode=True)

        # otherwise its one of the other options, like search etc
    for key, val in other_choices.items():
        formatted_metadata[key] = \
            yaml.dump({
                key: val['explanation']},
                allow_unicode=True)

    logger.debug('formatted data is %s' % formatted_metadata)
    return formatted_metadata


def _import(file_type_object, choice, move_file):
    path_in_library = _copy_to_library(file_type_object, choice, move_file)
    if path_in_library:
        book = add_book_to_db(file_type_object, choice, path_in_library)
        click.secho('imported %s - %s' % (book.authors_names, book.title), fg='green')
        return book
    else:
        click.secho('could not import %s' % file_type_object.path, fg='red')
