
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from .. import db, whooshee

@whooshee.register_model('name')
class Author(db.Model):
    __tablename__ = 'authors'
    __searchable__ = ['name']

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship("Book",
                         secondary="book_author_association",
                         back_populates="authors",
                         cascade_backrefs=False  # dont cascade to this authors books to prevent adding books from cache
                         )

    def __repr__(self):
        return '<{name}>'.format(name=self.name)