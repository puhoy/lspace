import datetime
import json

from sqlalchemy import Column, String, DateTime, Text, Integer

from lspace import db


class MetaCache(db.Model):
    __tablename__ = 'meta_cache'

    id = Column(Integer, primary_key=True)
    isbn = Column(String(13))
    service = Column(String(10))
    date = Column(DateTime(), default=datetime.datetime.now())

    # sqlite doesnt like json, and we dont want to run queries on json keys,
    # so we just use text and parse.
    data = Column(Text())

    @property
    def results(self):
        results = json.loads(self.data)
        return results

    @results.setter
    def results(self, results):
        data = json.dumps(results)
        self.data = data
