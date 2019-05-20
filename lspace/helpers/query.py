import json

import isbnlib

from lspace import db
from lspace.helpers import logger
from lspace.models.meta_cache import MetaCache


def _get_metadata_for_isbn(isbn, service='openl') -> dict:
    cached_meta = MetaCache.query.filter_by(isbn=isbn, service=service).first()
    if cached_meta:
        return json.loads(cached_meta.data)
    else:
        try:
            meta = isbnlib.meta(isbn, service=service, cache='default')
        except (isbnlib.dev._exceptions.NoDataForSelectorError,
                isbnlib._exceptions.NotValidISBNError,
                isbnlib.dev._exceptions.DataNotFoundAtServiceError
                ):
            meta = {}
        new_meta = MetaCache(isbn=isbn, service=service, data=json.dumps(meta))

        db.session.add(new_meta)
        db.session.commit()
    return meta


def query_isbn_data(isbn_str) -> dict:
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
