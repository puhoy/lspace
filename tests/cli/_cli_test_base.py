import os
import shutil
import tempfile
import unittest

from flask_migrate import upgrade

from lspace import create_app
from lspace.models import Book, Author


def get_test_app(test_dir):
    return create_app(app_dir=test_dir)


def get_temp_dir():
    return tempfile.mkdtemp()


class BaseCliTest(unittest.TestCase):

    def setUp(self):

        self.test_dir = get_temp_dir()
        self.app = get_test_app(self.test_dir)
        self.app.config['USER_CONFIG']['library_path'] = os.path.join(self.test_dir, 'library')

        print(self.app.config['USER_CONFIG'])

        self.test_author_name = 'testname'
        self.test_title = 'testtitle'
        self.test_path = '/some/path.ext'

        self.test_author = Author(name=self.test_author_name)
        self.test_book = Book(authors=[self.test_author], title=self.test_title, path=self.test_path)

        with self.app.app_context():
            upgrade()
            from lspace import db
            db.session.add(self.test_author)
            db.session.add(self.test_book)
            db.session.commit()

    def tearDown(self):
        shutil.rmtree(self.test_dir)
