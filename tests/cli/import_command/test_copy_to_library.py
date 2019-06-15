import os
from unittest.mock import MagicMock

from lspace.cli.import_command import copy_to_library
from lspace.models import Book
from tests.cli._cli_test_base import BaseCliTest


class TestCopyToLibrary_Move(BaseCliTest):

    def test_copy_to_library(self):
        with self.app.app_context():
            book = Book.query.first()
            old_path = book.path
            new_path = 'new_path'
            absolute_library_path = os.path.join(self.app.config['USER_CONFIG']['library_path'], new_path)

            copy_to_library.move = MagicMock(return_value=None)
            copy_to_library.copyfile = MagicMock(return_value=None)

            copy_to_library.find_unused_path = MagicMock(return_value=new_path)

            copy_to_library.copy_to_library(book.path, book, move_file=True)
            copy_to_library.move.assert_called_with(old_path, absolute_library_path)
            copy_to_library.copyfile.assert_not_called()


class TestCopyToLibrary_Copy(BaseCliTest):

    def test_copy_to_library_copy(self):
        with self.app.app_context():
            book = Book.query.first()
            old_path = book.path
            new_path = 'new_path'

            absolute_library_path = os.path.join(self.app.config['USER_CONFIG']['library_path'], new_path)

            copy_to_library.move = MagicMock(return_value=None)
            copy_to_library.copyfile = MagicMock(return_value=None)

            copy_to_library.find_unused_path = MagicMock(return_value=new_path)

            copy_to_library.copy_to_library(book.path, book, move_file=False)
            copy_to_library.move.assert_not_called()

            copy_to_library.copyfile.assert_called_with(old_path, absolute_library_path)
