from lspace.cli.tools_command import update_paths as update_paths_module

from lspace.file_types import FileTypeBase
from lspace.models import Book
from tests.cli._cli_test_base import BaseCliTest

from unittest.mock import MagicMock


class TestToolsUpdatePathsCommand(BaseCliTest):

    def test_update_path(self):
        with self.app.app_context():
            book = Book.query.first()

            test_new_path = 'new_path'
            file_type_object_mock = FileTypeBase(book.path)

            update_paths_module.copy_to_library = MagicMock(return_value=test_new_path)
            update_paths_module.get_file_type_object = MagicMock(return_value=file_type_object_mock)

            new_path = update_paths_module.update_path(book)

            assert test_new_path == new_path
            assert book.path == new_path

    def test_update_paths(self):
        with self.app.app_context():
            update_paths_module.update_path = MagicMock(return_value='asdasd')
            book = Book.query.first()

            runner = self.app.test_cli_runner()

            result = runner.invoke(update_paths_module._update_paths)

            assert result.exit_code == 0

            update_paths_module.update_path.assert_called_with(book)

            assert 'moved ' in result.output
