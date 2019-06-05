
import logging

from lspace import db
from lspace.file_types import FileTypeBase
from lspace.helpers.search_result import SearchResult
from lspace.models import Author, Book

logger = logging.getLogger(__name__)

def add_book_to_db(file_type_object, result, path_in_library):
    # type: (FileTypeBase, SearchResult, str) -> Book
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen metadata result
    :param path_in_library: the path after import
    :return:
    """
    authors = []
    for author_name in result.authors:
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            logger.info('creating %s' % author_name)
            author = Author(name=author_name)
            db.session.add(author)
        authors.append(author)

    title = result.title
    isbn13 = result.isbn
    publisher = result.publisher
    year = result.year
    language = result.language

    book = Book(
        title=title,
        authors=authors,
        publisher=publisher,
        year=year,
        language=language,
        md5sum=file_type_object.get_md5(),
        path=path_in_library,
        isbn13=isbn13
    )
    logger.info('adding book %s' % book)
    db.session.add(book)
    db.session.commit()
    return book
