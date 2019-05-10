from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from . import Base

book_author_association_table = Table('book_author_association', Base.metadata,
                                      Column('book_id', Integer,
                                             ForeignKey('books.id')),
                                      Column('author_id', Integer,
                                             ForeignKey('authors.id'))
                                      )
