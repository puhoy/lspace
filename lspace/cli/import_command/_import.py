import copy
import logging

import click
import yaml

from lspace.cli.import_command.add_book_to_db import add_book_to_db
from lspace.cli.import_command.copy_to_library import _copy_to_library

from lspace.file_types import get_file_type_class
from lspace.models import Book

from lspace.cli.import_command.options import other_choices

logger = logging.getLogger(__name__)


def bold(s):
    return click.style(s, bold=True)


def search_method_generator(methods):
    while True:
        got_something = False
        for description, find_function in methods.items():
            click.echo(bold(description))
            res = find_function()
            if res:
                got_something = True
                yield res
            else:
                click.echo('no results :(')

        if not got_something:
            yield []


def guided_import(path, skip_library_check, move):
    click.echo(bold('importing ') + path)
    FileClass = get_file_type_class(path)
    if FileClass:
        try:
            f = FileClass(path)
        except Exception as e:
            logger.exception(f'error reading {path}', exc_info=True)
            click.secho(f'error reading {path}', fg='red')
            return

        if not skip_library_check and Book.query.filter_by(md5sum=f.get_md5()).first():
            click.echo(bold('already imported') + ', skipping...')
            return

        search_generator = search_method_generator(f.get_find_functions())

        isbns_with_metadata = next(search_generator)

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
                                                                 search_generator=search_generator)

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
            click.style(f'\n{idx + 1}: {authors} - {title}\n', bold=True) + yaml.dump(meta, allow_unicode=True)

        # otherwise its one of the other options, like search etc
    for key, val in other_choices.items():
        formatted_metadata[key] = \
            click.style(yaml.dump({
                key: val['explanation']},
                allow_unicode=True), bold=True)

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
