import click

from lspace.cli.import_command.base_helper import BaseHelper
from lspace.helpers.query import query_isbn_data


class ISBNLookup(BaseHelper):
    explanation = 'search by isbn'

    @classmethod
    def function(cls, *args, **kwargs):
        isbn_str = click.prompt(
            'specify isbn (without whitespaces, only the number)')
        result = query_isbn_data(isbn_str)
        if result:
            return [result]
        return []
