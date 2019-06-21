import unittest
import xml.etree.ElementTree as ET
from lspace.cli.import_command.import_from_calibre import CalibreMetaFile
from tests.cli._cli_test_base import BaseCliTest

title = 'testtitle'
year = 1960
date = "{year}-02-14T23:00:00+00:00".format(year=year)
publisher = "testpublisher"
isbn = "some_isbn"
language = 'testlang'
author = 'some author'

testfile = """<?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title>{TITLE}</dc:title>
        <dc:creator opf:file-as="" opf:role="aut">{AUTHOR}</dc:creator>
        <dc:date>{DATE}</dc:date>
        <dc:publisher>{PUBLISHER}</dc:publisher>
        <dc:identifier opf:scheme="ISBN">{ISBN}</dc:identifier>
        <dc:language>{LANGUAGE}</dc:language>
    </metadata>
    <guide>
        <reference href="cover.jpg" title="Cover" type="cover"/>
    </guide>
</package>
    """.format(TITLE=title, DATE=date, PUBLISHER=publisher, ISBN=isbn, LANGUAGE=language, AUTHOR=author)


class BookTest(BaseCliTest):

    def test_meta_file(self):
        calibre_meta = CalibreMetaFile(xml=testfile)

        assert calibre_meta.title == title
        assert calibre_meta.year == year
        assert calibre_meta.publisher == publisher
        assert calibre_meta.isbn == isbn
        assert calibre_meta.language == language
        assert calibre_meta.authors == [author]

    def test_meta_book(self):
        calibre_meta = CalibreMetaFile(xml=testfile)
        with self.app.app_context():
            book = calibre_meta.get_book()

            assert book.title == title
            assert book.year == year
            assert book.publisher == publisher
            assert book.isbn13 == isbn
            assert book.language == language
            assert book.authors_names == author
