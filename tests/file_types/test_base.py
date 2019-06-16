import unittest
from unittest.mock import MagicMock

from lspace.file_types import FileTypeBase
from lspace.file_types import _base


class FileTypeBaseTest(unittest.TestCase):

    def test_filename(self):
        test_path = '/tmp/test/'
        test_filename = 'testfile.pdf'
        f = FileTypeBase(test_path + test_filename)

        assert f.filename == test_filename

    def test_filter_symbols(self):
        test_str = 'a-.$/bc'
        expected_output = 'a    bc'

        f = FileTypeBase('')

        assert f._filter_symbols(test_str) == expected_output

    def test_clean_filename(self):
        test_path = '/tmp/test/some_filename.ext'
        expected_output = 'some filename'

        f = FileTypeBase(test_path)

        assert f._clean_filename() == expected_output

    def test_get_isbn_from_text(self):
        f = FileTypeBase('')

        expected_isbn = '9783161484100'

        test_text = [
            'page 1',
            'page 2 978-3-16-148410-0 still page 2',
            'page 3'
        ]
        f.get_text = MagicMock(return_value=test_text)
        isbns = f.get_isbns_from_text()
        assert isbns == [expected_isbn]

        test_text = [
            'page 1',
            'page 2 ISBN 978-3-16-148410-0 still page 2',
            'page 3'
        ]
        f.get_text = MagicMock(return_value=test_text)
        isbns = f.get_isbns_from_text()
        assert isbns == [expected_isbn]

        test_text = [
            'page 1',
            'page 2 9783161484100 still page 2',
            'page 3'
        ]
        f.get_text = MagicMock(return_value=test_text)
        isbns = f.get_isbns_from_text()
        assert isbns == [expected_isbn]

    def test_find_isbn_in_text(self):
        f = FileTypeBase('')

        expected_metadata = {
            'a': 1
        }

        test_text = [
            'page 1',
            'page 2 978-3-16-148410-0 still page 2',
            'page 3'
        ]
        f.get_text = MagicMock(return_value=test_text)
        _base.query_isbn_data = MagicMock(return_value=expected_metadata)

        isbns = f.find_isbn_in_text()
        assert isbns == [expected_metadata]


    def test_find_isbn_in_metadata(self):
        f = FileTypeBase('')

        expected_metadata = {
            'a': 1
        }
        test_text = '978-3-16-148410-0'

        f.get_isbn = MagicMock(return_value=test_text)
        _base.query_isbn_data = MagicMock(return_value=expected_metadata)

        isbns = f.find_isbn_in_metadata()
        assert isbns == [expected_metadata]
