import click

from lspace.helpers import query_isbn_data


def lookup_isbn():
    isbn_str = click.prompt(
        'specify isbn (without whitespaces, only the number)')
    result = query_isbn_data(isbn_str)
    if result:
        return [result]
    return []
