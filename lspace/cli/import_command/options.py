from copy import deepcopy

import click
import yaml

from lspace.file_types import FileTypeBase
from lspace.helpers import preprocess_isbns
from lspace.helpers.query import query_isbn_data, query_google_books
from lspace.models import Book, Shelve


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


def manual_import(file_type_object, *args, **kwargs):
    # type: (FileTypeBase, [], {}) -> [dict]
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
        text = '# import {file_type_object.path}\n'.format(file_type_object=file_type_object)
        text += '# only the title is needed, but you probably want to specify more :)\n\n'
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

                return [Book.from_search_result(result, metadata_source='manually added')]


def put_in_new_shelve(book, *args, **kwargs):
    # type: (Book, list, dict) -> Book
    while True:
        shelve_name = click.prompt(
            'whats the name of the new shelve?')
        existing_shelve = Shelve.query.filter_by(name=shelve_name).first()
        if not existing_shelve:
            shelve = Shelve(name=shelve_name)
        else:
            if click.confirm('shelve with this name already exists - put book in this shelve?'):
                shelve = existing_shelve
            else:
                continue
        book.shelve = shelve
        return book


def put_in_default_shelve(book, *args, **kwargs):
    # type: (Book, list, dict) -> Book
    book.shelve = None
    return book


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
    'm': dict(
        function=manual_import,
        explanation='import manually'),
    's': dict(
        function=skip_book_function,
        explanation='skip this book'),
}

choose_shelve_other_choices = {
    'n': dict(
        function=put_in_new_shelve,
        explanation='add to new shelve'
    ),
    'd': dict(
        function=put_in_default_shelve,
        explanation='use default shelve'
    )
}
