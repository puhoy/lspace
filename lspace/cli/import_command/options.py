import click

from lspace.helpers import query_google_books
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
    's': dict(
        function=skip_book_function,
        explanation='skip this book'),
}
