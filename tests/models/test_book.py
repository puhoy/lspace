

import os
import shutil
import tempfile
import unittest

from flask_migrate import upgrade

from lspace import create_app, db
from lspace.models import Book, Author


def get_test_app(test_dir):
    return create_app(app_dir=test_dir)


def get_temp_dir():
    return tempfile.mkdtemp()


class BookTest(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = get_temp_dir()

    def getApp(self):

        app = get_test_app(self.test_dir)
        app.config['USER_CONFIG']['library_path'] = os.path.join(self.test_dir, 'library')

        with app.app_context():
            upgrade()
            from lspace import db
            db.session.commit()
        return app

    def tearDown(self):
        shutil.rmtree(self.test_dir)


    def test_book_adding(self):
        """
        adding a book should cascade to author,
        but author should not cascade to 2nd book

        :return:
        """
        with self.getApp().app_context():
            author = Author(name='author')
            book_1 = Book(title='book_1', authors=[author])
            book_2 = Book(title='book_2', authors=[author])

            db.session.add(book_1)

            db.session.commit()
            db.session.flush()

        with self.getApp().app_context():
            books = Book.query.all()
            assert len(books) == 1
            assert books[0].authors[0].name == 'author'


    def test_author_adding_2(self):
        """
        adding an author should not cascade to books

        :return:
        """
        with self.getApp().app_context():
            author = Author(name='author')
            book_1 = Book(title='book_1', authors=[author])
            book_2 = Book(title='book_2', authors=[author])

            db.session.add(author)

            db.session.commit()
            db.session.flush()

        with self.getApp().app_context():
            books = Book.query.all()
            assert len(books) == 0
            author = Author.query.all()
            assert len(author) == 1

    # todo: test cascading with shelve
