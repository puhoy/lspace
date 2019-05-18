from copy import deepcopy

import click
import yaml

from lspace.file_types import FileTypeBase
from lspace.helpers import query_google_books, preprocess_isbns
from lspace.helpers import query_isbn_data


def try_next_results(search_generator, *args, **kwargs):
    return next(search_generator)


def peek_function(file_type_object, old_choices, *args, **kwargs):
    click.echo_via_pager(file_type_object.get_text())
    return old_choices


def run_search_function(*args, **kwargs):
    search_string = click.prompt('search string')
    return query_google_books(search_string)


def skip_book_function(*args, **kwargs):
    return False


def lookup_isbn_function(*args, **kwargs):
    isbn_str = click.prompt(
        'specify isbn (without whitespaces, only the number)')
    result = query_isbn_data(isbn_str)
    if result:
        return [result]
    return []


def manual_import(file_type_object: FileTypeBase, *args, **kwargs):
    _edit_dict = dict(
        Title='',
        Authors=['', ],
        ISBN='',
        Publisher='',
        Year='',
        Language='',
    )

    edit_dict = deepcopy(_edit_dict)

    while True:
        text = f'# import {file_type_object.path}\n'
        text += f'# only the title is needed, but you probably want to specify more :)\n\n'
        text += yaml.dump(edit_dict, sort_keys=False)

        result = click.edit(text, require_save=True)
        if not result:
            click.pause('no data! did you save?')
        else:
            result = yaml.load(result, Loader=yaml.FullLoader)
            if not result['Title']:
                choice = ''
                while choice not in ['e', 'r']:
                    choice = click.prompt('title is needed! \n'
                                          'e: edit\n'
                                          'p: ' + other_choices['p']['explanation'] + '\n' +
                                          'r: restart with empty form\n',
                                          type=click.Choice(['e', 'r', 'p']), default='e')
                    if choice == 'e':
                        edit_dict = result

                    elif choice == 'r':
                        edit_dict = deepcopy(_edit_dict)
                    else:
                        other_choices['p']['function'](file_type_object, [])
            else:
                isbn = result.get('ISBN')
                if isbn:
                    isbns = preprocess_isbns([isbn])
                    if len(isbns) == 1:
                        isbn = isbns[0]
                        result['ISBN-13'] = isbn

                return [result]


other_choices = {
    'q': dict(
        function=run_search_function,
        explanation='run manual query'),
    'i': dict(
        function=lookup_isbn_function,
        explanation='search by isbn'),
    'p': dict(
        function=peek_function,
        explanation='peek in the text'),
    't': dict(
        function=try_next_results,
        explanation='try to get more results'),
    'm': dict(
        function=manual_import,
        explanation='import manually'),
    's': dict(
        function=skip_book_function,
        explanation='skip this book'),
}
