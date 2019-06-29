from lspace.cli.import_command.base_helper import BaseHelper
from lspace.models import Book


class PutInDefaultShelf(BaseHelper):
    explanation = 'add to default shelf'

    @classmethod
    def function(cls, book, *args, **kwargs):
        # type: (Book, list, dict) -> Book
        book.shelf = None
        return book

