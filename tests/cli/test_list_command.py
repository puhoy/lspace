import os

from lspace.cli import list_command
from tests.cli._cli_test_base import BaseCliTest


class TestList(BaseCliTest):

    def test_list_command_simple(self):
        runner = self.app.test_cli_runner()

        result = runner.invoke(list_command._list, [])

        assert result.exit_code == 0

        print(result.output)

        assert '{author} - {title}'.format(author=self.test_author_name, title=self.test_title) in result.output

    def test_list_command_details(self):
        runner = self.app.test_cli_runner()

        result = runner.invoke(list_command._list, ['--details'])

        assert result.exit_code == 0

        assert '{author} - {title}'.format(author=self.test_author_name, title=self.test_title) in result.output
        assert 'language: ' in result.output
        assert 'year: ' in result.output
        assert 'isbn: ' in result.output

    def test_list_command_path(self):
        runner = self.app.test_cli_runner()

        result = runner.invoke(list_command._list, ['--path'])

        assert result.exit_code == 0

        assert os.path.join(self.test_dir, self.test_path) in result.output
