import os

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .. import db, whooshee
from flask import current_app

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
        return f'{os.path.join(current_app.config["LIBRARY_PATH"], self.path)}'

    @property
    def authors_names(self) -> str:
        return ', '.join(author.name for author in self.authors)

    @property
    def extension(self) -> str:
        filename, file_extension = os.path.splitext(self.full_path)
        return file_extension


