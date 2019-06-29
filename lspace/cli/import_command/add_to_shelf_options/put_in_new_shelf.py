import click

from lspace.cli.import_command.base_helper import BaseHelper
from lspace.models import Book, Shelf


class PutInNewShelf(BaseHelper):
    explanation = 'add to new shelf'

    @classmethod
    def function(cls, book, *args, **kwargs):
        # type: (Book, list, dict) -> Book
        while True:
            shelf_name = click.prompt(
                'whats the name of the new shelf?')
            existing_shelf = Shelf.query.filter_by(name=shelf_name).first()
            if not existing_shelf:
                shelf = Shelf(name=shelf_name)
            else:
                if click.confirm('shelf with this name already exists - put book in this shelf?'):
                    shelf = existing_shelf
                else:
                    continue
            book.shelf = shelf
            return book

