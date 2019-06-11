from lspace.cli.init_command import init
from tests.cli._cli_test_base import BaseCliTest


class TestInitCommand(BaseCliTest):

    def test_init_command(self):
        runner = self.app.test_cli_runner()

        # invoke the command directly
        result = runner.invoke(init, [])
        assert result.exit_code == 0
        assert 'written config file to ' in result.output
        assert self.test_dir in result.output
