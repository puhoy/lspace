from typing import List

import ebooklib
import html2text
import isbnlib
from ebooklib import epub

from ._base import FileTypeBase


class Epub(FileTypeBase):
    extension = '.epub'

    def __init__(self, path):
        super().__init__(path)
        self.book = epub.read_epub(path)

    def get_text(self) -> List[str]:
        text = []

        for doc in self.book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            content = doc.get_content().decode('utf-8')
            text.append(html2text.html2text(content))
        if True in [bool(t) for t in text]:
            return text
        return []

    def get_author(self):
        _author = self.book.get_metadata('DC', 'creator')
        # [('Firstname Lastname ', {})]
        if _author:
            return _author[0][0]
        return None

    def get_title(self):
        _title = self.book.get_metadata('DC', 'title')
        # [('Ratio', {})]
        if _title:
            return _title[0][0]
        return None

    def get_isbn(self):
        _isbn = self.book.get_metadata('DC', 'identifier')
        # [('Ratio', {})]
        if _isbn:
            isbn = _isbn[0][0]
            if isbnlib.notisbn(isbn):
                return None
            if isbnlib.is_isbn10(isbn):
                return isbnlib.to_isbn13(isbn)
            return isbn
        return None
