import hashlib
import logging
import os
import string

import isbnlib

from lspace.helpers import preprocess_isbns
from lspace.helpers.query import query_isbn_data, query_google_books

logger = logging.getLogger(__name__)


class FileTypeBase:
    extension = None

    def __init__(self, path):
        self.path = path

    def get_text(self):
        raise NotImplementedError

    def get_title(self):
        return None

    def get_author(self):
        return None

    def get_year(self):
        return None

    def get_isbn(self):
        return None

    @property
    def filename(self):
        filename = os.path.split(self.path)[-1]
        return filename

    def get_md5(self):
        with open(self.path, 'rb') as file_to_check:
            data = file_to_check.read()
            md5sum = hashlib.md5(data).hexdigest()
        logger.debug('md5 is %s' % md5sum)
        return md5sum

    def find_isbn_in_metadata(self):
        _isbn = self.get_isbn()
        if _isbn:
            logger.info('found isbn %s in metadata!' % _isbn)
            d = query_isbn_data(_isbn)
            if d:
                return [d]
        return []

    def find_isbn_in_text(self):
        logger.info('looking for isbn in text...')
        isbns = self.get_isbns_from_text()
        if isbns:
            isbns_with_metadata = []
            for isbn in isbns:
                d = query_isbn_data(isbn)
                if d:
                    isbns_with_metadata.append(d)

            if isbns_with_metadata:
                logger.info('found isbns in text!')
                return isbns_with_metadata
        return []

    def find_isbn_from_author_title(self):
        if self.get_title():
            search_str = self._filter_symbols(self.get_title())
            if self.get_author():
                search_str = '%s %s' % (self._filter_symbols(self.get_author()), search_str)
            results = query_google_books(search_str)
            if results:
                logger.info('found isbns from author + title...')
                return results
        return []

    def find_isbn_from_filename(self):
        guessed_meta = self.guess_from_filename()
        if guessed_meta:
            return guessed_meta
        return []

    def fetch_results(self):
        find_functions = [self.find_isbn_in_metadata,
                          self.find_isbn_in_text,
                          self.find_isbn_from_author_title,
                          self.find_isbn_from_filename]
        results = {}
        for f in find_functions:
            for result in f():
                results[result.isbn13] = result
        self.results = list(results.values())
        return self.results


    def _filter_symbols(self, s):
        # type: (str) -> str
        whitelist = string.ascii_letters + string.digits + ' '
        clean_string = ''.join(
            c if c in whitelist else ' ' for c in s)
        return clean_string

    def _clean_filename(self):
        filename, extension = os.path.splitext(self.filename)
        clean_filename = self._filter_symbols(filename)

        return clean_filename

    def guess_from_filename(self):
        clean_filename = self._clean_filename()
        logger.info('looking for %s' % clean_filename)
        results = query_google_books(clean_filename)
        logger.debug('results: %s' % results)
        return results

    def get_isbns_from_text(self):
        pages = self.get_text()
        pages_as_str = '\n'.join(pages)

        isbns = isbnlib.get_isbnlike(pages_as_str, level='normal')

        # print('unprocessed isbns: %s' % isbns)
        canonical_isbns = preprocess_isbns(isbns)

        # print('canonical isbns: %s' % canonical_isbns)
        return canonical_isbns
