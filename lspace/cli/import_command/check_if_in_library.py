import logging

from typing import Set

from lspace import db
from lspace.models import Book

logger = logging.getLogger(__name__)



def check_if_in_library(result):
    # type: (Book) -> Set[Book]
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen metadata result
    :param path_in_library: the path after import
    :return:
    """

    title = result.title
    isbn13 = result.isbn13
    publisher = result.publisher
    year = result.year
    language = result.language


    if isbn13:
        books = Book.query.filter_by(isbn13=isbn13).all()
    else:
        books = []
    books += Book.query.filter(Book.title.ilike(title.replace(' ', '%')) ).distinct()
    return set(books)
