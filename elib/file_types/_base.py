import os
import string
import logging

import isbnlib


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

    def find_in_db(self):
        # based on isbns from text
        logging.info('processing %s' % self.path)
        logging.info('getting from text...')
        isbns = self.get_isbns_from_text()
        if isbns:
            isbns_with_metadata = []
            for isbn in isbns:
                try:
                    isbns_with_metadata.append(isbnlib.meta(
                        isbn, service='default', cache='default'))
                except Exception as e:
                    logging.error(e, exc_info=True)
            return isbns_with_metadata

        # if author + title:
        logging.info('getting from author + title...')
        if self.get_author() and self.get_title():
            return isbnlib.goom(self._clean_filename())

        # from filename
        logging.info('getting from filename...')
        guessed_meta = self.guess_from_filename()
        if guessed_meta:
            return guessed_meta
        return []

    def _clean_filename(self):
        filename = os.path.split(self.path)[-1]
        filename, extension = os.path.splitext(filename)

        whitelist = string.ascii_letters + string.digits + ' '
        clean_filename = ''.join(
            c if c in whitelist else ' ' for c in filename)

        return clean_filename

    def guess_from_filename(self):
        print('looking for %s' % self._clean_filename())
        results = isbnlib.goom(self._clean_filename())
        logging.info('results: %s' % results)
        return results
        

    def get_metadata_for_isbn(self, isbn):
        try:
            meta = isbnlib.meta(isbn, service='default', cache='default')
        except isbnlib.dev._exceptions.NoDataForSelectorError:
            meta = {}
        return meta

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
