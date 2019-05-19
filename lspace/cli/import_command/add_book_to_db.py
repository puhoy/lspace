
import logging

from lspace import db
from lspace.models import Author, Book

logger = logging.getLogger(__name__)

def add_book_to_db(file_type_object, result, path_in_library):
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen metadata result
    :param path_in_library: the path after import
    :return:
    """
    authors = []
    for author_name in result['Authors']:
        author = Author.query.filter_by(name=author_name).first()
        if not author:
            logger.info('creating %s' % author_name)
            author = Author(name=author_name)
            db.session.add(author)
        authors.append(author)

    title = result['Title']
    isbn13 = result.get('ISBN-13', '')
    publisher = result.get('Publisher', '')
    year = result.get('Year', '')
    language = result.get('Language', '')

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
