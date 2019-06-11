import logging
import os

from flask import current_app
from slugify import slugify
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lspace import db, whooshee
from lspace.models import Author

logger = logging.getLogger(__name__)


@whooshee.register_model('title', 'language', 'isbn13')
class Book(db.Model):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    authors = relationship("Author",
                           secondary="book_author_association",
                           backref="authors_books")
    isbn13 = Column(String(13))
    publisher = Column(String(100))
    year = Column(Integer())
    language = Column(String(20))

    md5sum = Column(String(32))
    path = Column(String(400))

    metadata_source = Column(String(20), default='')

    @property
    def full_path(self):
        # type: () -> str
        library_path = current_app.config['USER_CONFIG']['library_path']
        return os.path.join(library_path, self.path)

    @property
    def authors_names(self):
        # type: () -> str
        return ', '.join(author.name for author in self.authors)

    @property
    def author_names_slug(self):
        author_slugs = [slugify(author.name) for author in self.authors]
        authors = '_'.join(author_slugs)
        return authors

    @property
    def title_slug(self):
        return slugify(self.title)

    @property
    def extension(self):
        # type: () -> str
        filename, file_extension = os.path.splitext(self.full_path)
        return file_extension

    @staticmethod
    def from_search_result(d, metadata_source):
        book = Book()
        book.metadata_source = metadata_source
        book.from_dict(d)
        return book

    def from_dict(self, d):
        self.isbn13 = d.get('ISBN-13', None)
        self.title = d.get('Title', 'no title')
        self.publisher = d.get('Publisher', None)
        self.year = int(d.get('Year', 'no year'))
        self.language = d.get('Language', None)

        if not d.get('Authors', None):
            authors = ['no author']
        else:
            authors = d.get('Authors')

        for author_name in authors:
            author = Author.query.filter_by(name=author_name).first()
            if not author:
                logger.info('creating %s' % author_name)
                author = Author(name=author_name)
            self.authors.append(author)

    def __repr__(self):
        return '<isbn={isbn} authors={authors} title={title}>'.format(isbn=self.isbn13, authors=self.authors_names,
                                                                      title=self.title)

    def to_dict(self):
        return dict(
            title=self.title,
            authors=self.authors,

            isbn13=self.isbn13,
            publisher=self.publisher,
            year=self.year,
            language=self.language,

            md5sum=self.md5sum,
            path=self.path,

            metadata_source=self.metadata_source
        )

    def formatted_output_head(self):
        return '{authors} - {title} ({year})'.format(
            authors=self.authors_names, title=self.title, year=self.year)

    def formatted_output_details(self):
        return 'isbn: {isbn}\npublisher: {publisher}\nlanguage: {language}\nmetadata source: {source}\n'.format(
            isbn=self.isbn13,
            language=self.language,
            publisher=self.publisher,
            source=self.metadata_source)

    def save(self):
        print(self)
        print('self id', self.id)

        db.session.add(self)

        return db.session.commit()
