import click

from lspace.helpers import query_google_books


def run_search():
    search_string = click.prompt('search string')
    return query_google_books(search_string)