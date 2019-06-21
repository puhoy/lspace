import sqlite3
import xml.etree.ElementTree as ET
from collections import namedtuple
from pathlib import Path

from typing import Generator
from typing import List
from dateutil.parser import parse
from lspace.models import Book, Author

CalibreBook = namedtuple('Book', ['path'])


class CalibreWrapper:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.library_path = Path(db_path).parent

    def get_library_id(self):
        query = """
        SELECT id, uuid
        FROM library_id;
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

    def import_books(self):
        """
        iterate over the books paths from calibre sqlite db,
        prepare book object from metadata.opf, yield this book object along with the path to the book
        (yields path/book per book file; calibre stores all formats of the book in this folder)
        
        :return: 
        """
        for book_path in self._get_book_paths():
            abs_book_path = Path(self.library_path, book_path)
            meta_file = str(Path(abs_book_path, 'metadata.opf'))

            calibre_meta = CalibreMetaFile(meta_file)
            book = calibre_meta.get_book()

            files_in_book_path = [str(p) for p in abs_book_path.glob('*') if
                                  not (str(p).endswith('metadata.opf') or str(p).endswith('cover.jpg'))]
            
            for file in files_in_book_path:
                yield file, book

    def _get_book_paths(self):
        # type: () -> Generator[List[str]]
        query = """
        SELECT books.path
        FROM books
        """
        cursor = self.conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            yield row[0]


class CalibreMetaFile:

    ns = {'dc': 'http://purl.org/dc/elements/1.1/',
          'opf': 'http://www.idpf.org/2007/opf'
          }

    def __init__(self, path=None, xml=None):
        if path:
            tree = ET.parse(path)
            self.root = tree.getroot()
        elif xml:
            self.root = ET.fromstring(xml)
        else:
            raise Exception('no path or xml provided!')


    @property
    def title(self):
        node = self.root[0].find('dc:title', CalibreMetaFile.ns)
        if node is None:
            return None
        return node.text

    @property
    def authors(self):
        nodes = self.root[0].findall('dc:creator', CalibreMetaFile.ns)
        return [node.text for node in nodes]

    @property
    def isbn(self):
        node = self.root[0].find('dc:identifier[@opf:scheme="ISBN"]', CalibreMetaFile.ns)
        if node is None:
            return None
        return node.text

    @property
    def publisher(self):
        node = self.root[0].find('dc:publisher', CalibreMetaFile.ns)
        if node is None:
            return None
        return node.text

    @property
    def year(self):
        node = self.root[0].find('dc:date', CalibreMetaFile.ns)
        if node is None:
            return None
        d = parse(node.text)
        return d.year

    @property
    def language(self):
        node = self.root[0].find('dc:language', CalibreMetaFile.ns)
        if node is None:
            return None
        return node.text
    
    def get_book(self):
        authors = []
        for author_name in self.authors:
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                author = Author()
                author.name = author_name
            authors.append(author)

        book = Book()
        book.from_dict({
            'Title': self.title,
            'ISBN-13': self.isbn,
            'Year': self.year,
            'Publisher': self.publisher,
            'Language': self.language
        })
        book.authors = authors
        book.metadata_source = 'calibre'
        return book