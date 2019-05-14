import hashlib
import logging
import os
import string

import isbnlib

from ..helpers import query_isbn_data, query_google_books

logger = logging.getLogger(__name__)


class FileTypeBase:
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

    def find_metadata(self):
        logger.info('processing %s' % self.path)

        # try isbn from metadata
        logger.info('looking for isbn in metadata...')
        _isbn = self.get_isbn()
        if _isbn:
            logger.info('found isbn %s in metadata!' % _isbn)
            d = query_isbn_data(_isbn)
            if d:
                return [d]

        # try find isbn in text
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

        
        # try from author + title in metadata:
        logger.info('getting from author + title...')
        if self.get_author() and self.get_title():
            results = query_google_books(self._clean_filename())
            if results:
                logger.info('found isbns from author + title...')
                return results

        # from filename
        logger.info('getting from filename...')
        guessed_meta = self.guess_from_filename()
        if guessed_meta:
            return guessed_meta
        
        return []

    def _clean_filename(self):
        filename, extension = os.path.splitext(self.filename)

        whitelist = string.ascii_letters + string.digits + ' '
        clean_filename = ''.join(
            c if c in whitelist else ' ' for c in filename)

        return clean_filename

    def guess_from_filename(self):
        clean_filename = self._clean_filename()
        logger.info('looking for %s' % clean_filename)
        results = isbnlib.goom(clean_filename)
        logger.debug('results: %s' % results)
        return results

    def _preprocess_isbns(self, isbns):
        """

        :param isbns: isbns in different formats
        :return: canonical isbn13s
        """
        canonical_isbns = []
        for isbn in isbns:
            if not isbnlib.notisbn(isbn, level='strict'):
                if isbnlib.is_isbn10(isbn):
                    isbn = isbnlib.to_isbn13(isbn)
                isbn = isbnlib.get_canonical_isbn(isbn)
                canonical_isbns.append(isbn)
        canonical_isbns = set(canonical_isbns)
        return list(canonical_isbns)

    def get_isbns_from_text(self):
        pages = self.get_text()
        pages_as_str = '\n'.join(pages)

        isbns = isbnlib.get_isbnlike(pages_as_str, level='normal')

        # print('unprocessed isbns: %s' % isbns)
        canonical_isbns = self._preprocess_isbns(isbns)

        # print('canonical isbns: %s' % canonical_isbns)
        return canonical_isbns
