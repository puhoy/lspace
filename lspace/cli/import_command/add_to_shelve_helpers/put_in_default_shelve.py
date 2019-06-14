from lspace.cli.import_command.base_helper import BaseHelper
from lspace.models import Book


class PutInDefaultShelve(BaseHelper):
    explanation = 'add to default shelve'

    @classmethod
    def function(cls, book, *args, **kwargs):
        # type: (Book, list, dict) -> Book
        book.shelve = None
        return book

