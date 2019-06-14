import click

from lspace.cli.import_command.base_helper import BaseHelper
from lspace.models import Book, Shelve


class PutInNewShelve(BaseHelper):
    explanation = 'add to new shelve'

    @classmethod
    def function(cls, book, *args, **kwargs):
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

