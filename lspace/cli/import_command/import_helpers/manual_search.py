import click

from lspace.cli.import_command.base_helper import BaseHelper
from lspace.helpers.query import query_google_books


class ManualSearch(BaseHelper):
    explanation = 'run manual query'

    @classmethod
    def function(cls, *args, **kwargs):
        search_string = click.prompt('search string')
        return query_google_books(search_string)
