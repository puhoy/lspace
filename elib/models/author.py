
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from . import Base


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    books = relationship("Book",
                         secondary="book_author_association",
                         back_populates="authors")
