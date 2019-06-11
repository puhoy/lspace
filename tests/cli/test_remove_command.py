from lspace.cli import remove_command
from tests.cli._cli_test_base import BaseCliTest


class TestListCommand(BaseCliTest):

    def test_remove(self):
        runner = self.app.test_cli_runner()

        result = runner.invoke(remove_command.remove, [self.test_title])

        assert result.exit_code == 0

        assert '{author} - {title}'.format(author=self.test_author_name, title=self.test_title) in result.output
