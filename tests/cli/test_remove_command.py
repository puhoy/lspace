import os
import shutil
import tempfile
import unittest

from flask_migrate import upgrade

from lspace import create_app
from lspace.cli import remove_command
from lspace.models import Book, Author


def get_test_app(test_dir):
    return create_app(app_dir=test_dir)


def get_temp_dir():
    return tempfile.mkdtemp()


class TestListCommand(unittest.TestCase):

    def setUp(self):

        self.test_dir = get_temp_dir()
        self.app = get_test_app(self.test_dir)
        self.app.config['USER_CONFIG']['library_path'] = os.path.join(self.test_dir, 'library')

        print(self.app.config['USER_CONFIG'])

        self.test_author_name = 'testname'
        self.test_title = 'testtitle'
        self.test_path = '/some/path'
        test_author = Author(name=self.test_author_name)
        test_book = Book(authors=[test_author], title=self.test_title, path=self.test_path)

        with self.app.app_context():
            upgrade()
            from lspace import db
            db.session.add(test_author)
            db.session.add(test_book)
            db.session.commit()

    def tearDown(self):
        shutil.rmtree(self.test_dir)


    def test_remove(self):
        runner = self.app.test_cli_runner()

        result = runner.invoke(remove_command.remove, [self.test_title])

        assert result.exit_code == 0


        assert '{author} - {title}'.format(author=self.test_author_name, title=self.test_title) in result.output
