import isbnlib
from typing import List

from lspace import db
from lspace.helpers import logger
from lspace.models.meta_cache import MetaCache
from lspace.models import Book, Author


def _fetch_isbn_meta(isbn, service):
    try:
        meta = isbnlib.meta(isbn, service=service, cache='default')
    except (isbnlib.dev._exceptions.NoDataForSelectorError,
            isbnlib._exceptions.NotValidISBNError,
            isbnlib.dev._exceptions.DataNotFoundAtServiceError
            ):
        meta = {}
    except Exception as e:
        logger.exception('failed to get isbn data from {service}: {error}'.format(error=e, service=service))
        meta = None
    return meta

def _get_metadata_for_isbn(isbn, service='openl'):
    # type: (str, str) -> Book
    cached_meta = MetaCache.query.filter_by(isbn=isbn, service=service).first()
    if cached_meta:
        meta = cached_meta.results
    else:
        meta = _fetch_isbn_meta(isbn, service)
        if meta != None:
            new_meta = MetaCache(isbn=isbn, service=service, results=meta)

            db.session.add(new_meta)
            db.session.commit()

    if meta:
        return Book.from_search_result(meta, metadata_source=service)
    return None


def query_isbn_data(isbn_str):
    # type: (str) -> Book

    if isbnlib.is_isbn10(isbn_str):
        isbn_str = isbnlib.to_isbn13(isbn_str)

    logger.info('query openlibrary for %s' % isbn_str)
    meta = _get_metadata_for_isbn(isbn_str, 'openl')

    if not meta:
        logger.info('query google books for %s' % isbn_str)
        meta = _get_metadata_for_isbn(isbn_str, 'goob')

    if meta:
        return meta
    return None


def query_google_books(words):
    # type: (str) -> [SearchResult]
    logger.debug('query google books for %s' % words)
    try:
        raw_results = isbnlib.goom(words)

    except isbnlib.dev._exceptions.NoDataForSelectorError as e:
        raw_results = []
    except Exception as e:
        logger.exception('failed to get from google books: {error}'.format(error=e))
        raw_results = []
    return [Book.from_search_result(result, metadata_source='google books api') for result in raw_results]


def query_db(query, books=True, authors=True):
    # type: (str, bool, bool) -> List[Book]
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
