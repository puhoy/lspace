
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..app import db


class Author(db.Model):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship("Book",
                         secondary="book_author_association",
                         back_populates="authors")
