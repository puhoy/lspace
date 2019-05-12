import os

from sqlalchemy import Column, Integer, String, Table
from sqlalchemy.orm import relationship

from ..app import db, whooshee
from ..config import library_path

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

    @property
    def full_path(self) -> str:
        return f'{os.path.join(library_path, self.path)}'

    @property
    def authors_names(self) -> str:
        return ', '.join(author.name for author in self.authors)


