

from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..app import db, whooshee

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


