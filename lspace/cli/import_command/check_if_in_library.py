import logging

from lspace import db
from lspace.models import Author, Book

logger = logging.getLogger(__name__)


def check_if_in_library(result):
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen metadata result
    :param path_in_library: the path after import
    :return:
    """

    title = result['Title']
    isbn13 = result.get('ISBN-13', '')
    publisher = result.get('Publisher', '')
    year = result.get('Year', '')
    language = result.get('Language', '')

    books = Book.query.whooshee_search(title, match_substrings=False).all()
    if isbn13:
        books += db.session.query(Book).filter_by(isbn13=isbn13).distinct()

    return set(books)
