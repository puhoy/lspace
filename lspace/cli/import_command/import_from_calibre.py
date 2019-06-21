import datetime
import sqlite3
import xml.etree.ElementTree as ET
from collections import namedtuple
from pathlib import Path

from typing import Generator
from typing import List

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
        for book_path in self._get_book_paths():
            abs_book_path = Path(self.library_path, book_path)
            meta_file = str(Path(abs_book_path, 'metadata.opf'))

            calibre_meta = CalibreMetaFile(meta_file)
            authors = []
            for author_name in calibre_meta.authors:
                author = Author.query.filter_by(name=author_name).first()
                if not author:
                    author = Author()
                    author.name = author_name
                authors.append(author)

            book = Book()
            book.from_dict({
                'Title': calibre_meta.title,
                'ISBN-13': calibre_meta.isbn,
                'Year': calibre_meta.year,
                'Publisher': calibre_meta.publisher,
                'Language': calibre_meta.language
            })
            book.authors = authors
            book.metadata_source = 'calibre'

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
    """
    <?xml version='1.0' encoding='utf-8'?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="uuid_id" version="2.0">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:identifier opf:scheme="calibre" id="calibre_id">1</dc:identifier>
        <dc:identifier opf:scheme="uuid" id="uuid_id">5353b127-4205-4217-9869-bbfb3a7e9797</dc:identifier>
        <dc:title>Schöne Neue Welt</dc:title>
        <dc:creator opf:file-as="Huxley, Aldous" opf:role="aut">Aldous Huxley</dc:creator>
        <dc:contributor opf:file-as="calibre" opf:role="bkp">calibre (3.44.0) [https://calibre-ebook.com]</dc:contributor>
        <dc:date>2007-02-14T23:00:00+00:00</dc:date>
        <dc:description>&lt;p class="description"&gt;Die schöne neue Welt, die Huxley hier beschreibt, ist die Welt einer konsequent verwirklichten Wohlstandsgesellschaft" im Jahre 632 nach Ford", einer Wohlstandsgesellschaft, in der alle Menschen am Luxus teilhaben, in der Unruhe, Elend und Krankheit überwunden, in der aber auch Freiheit, Religion, Kunst und Humanität auf der Strecke geblieben sind. Eine totale Herrschaft garantiert ein genormtes Glück. In dieser vollkommen" formierten"Gesellschaft erscheint jede Art von Individualismus als" asozial", wird als" Wilder"betrachtet, wer - wie einer der rebellischen Außenseiter dieses Romans - für sich fordert:" Ich brauche keine Bequemlichkeit. Ich will Gott, ich will Poesie, ich will wirkliche Gefahren und Freiheit und Tugend. Ich will Sünde!"&lt;/p&gt;</dc:description>
        <dc:publisher>Fischer Taschenbuch Vlg.</dc:publisher>
        <dc:identifier opf:scheme="AMAZON">3596200261</dc:identifier>
        <dc:identifier opf:scheme="GOOGLE">txdEygAACAAJ</dc:identifier>
        <dc:identifier opf:scheme="ISBN">9783596903450</dc:identifier>
        <dc:language>deu</dc:language>
        <dc:subject>Roman</dc:subject>
        <dc:subject>Science Fiction</dc:subject>
        <meta content="{&quot;Aldous Huxley&quot;: &quot;&quot;}" name="calibre:author_link_map"/>
        <meta content="10" name="calibre:rating"/>
        <meta content="2019-06-19T20:35:53.846581+00:00" name="calibre:timestamp"/>
        <meta content="Schöne Neue Welt" name="calibre:title_sort"/>
    </metadata>
    <guide>
        <reference href="cover.jpg" title="Cover" type="cover"/>
    </guide>
</package>
    """
    ns = {'dc': 'http://purl.org/dc/elements/1.1/',
          'opf': 'http://www.idpf.org/2007/opf'
          }

    def __init__(self, path):
        tree = ET.parse(path)
        self.root = tree.getroot()

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
        d = datetime.datetime.fromisoformat(node.text)
        return d.year

    @property
    def language(self):
        node = self.root[0].find('dc:language', CalibreMetaFile.ns)
        if node is None:
            return None
        return node.text