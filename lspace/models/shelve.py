import logging

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from lspace import db

logger = logging.getLogger(__name__)


class Shelve(db.Model):
    __tablename__ = 'shelves'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))

    books = relationship("Book", back_populates="shelve", cascade="")
