import isbnlib

from lspace import db
from lspace.helpers import logger
from lspace.models.meta_cache import MetaCache


def _get_metadata_for_isbn(isbn, service='openl'):
    # type: (str, str) -> dict
    cached_meta = MetaCache.query.filter_by(isbn=isbn, service=service).first()
    if cached_meta:
        return cached_meta.results
    else:
        try:
            meta = isbnlib.meta(isbn, service=service, cache='default')
        except (isbnlib.dev._exceptions.NoDataForSelectorError,
                isbnlib._exceptions.NotValidISBNError,
                isbnlib.dev._exceptions.DataNotFoundAtServiceError
                ):
            meta = {}
        new_meta = MetaCache(isbn=isbn, service=service, results=meta)

        db.session.add(new_meta)
        db.session.commit()
    return meta


def query_isbn_data(isbn_str):
    # type: (str) -> dict
    if isbnlib.is_isbn10(isbn_str):
        isbn_str = isbnlib.to_isbn13(isbn_str)

    logger.info('query openlibrary for %s' % isbn_str)
    meta = _get_metadata_for_isbn(isbn_str, 'openl')

    if not meta:
        logger.info('query google books for %s' % isbn_str)
        meta = _get_metadata_for_isbn(isbn_str, 'goob')

    if meta:
        return meta
    else:
        return None


def query_google_books(words):
    logger.debug('query google books for %s' % words)
    try:
        results = isbnlib.goom(words)

    except isbnlib.dev._exceptions.NoDataForSelectorError as e:
        results = []
    return results


def query_db(query, books=True, authors=True):
    from ..models import Book, Author
    if not query or (len(query) == 1 and not query[0]):  # in case of ('', )
        return Book.query.all()
    else:
        results = []
        joined_query = ' '.join(query)
        if books:
            results = Book.query.whooshee_search(joined_query, match_substrings=False).all()
        if authors:
            author_results = Author.query.whooshee_search(joined_query, match_substrings=False).all()
            for author in author_results:
                for book in author.books:
                    results.append(book)
    return results
