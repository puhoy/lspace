from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lspace import db, whooshee


@whooshee.register_model('name')
class Author(db.Model):
    __tablename__ = 'authors'
    __searchable__ = ['name']

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship("Book",
                         secondary="book_author_association",
                         back_populates="authors",
                         cascade=""
                         )

    def __repr__(self):
        return '<{name}>'.format(name=self.name)
