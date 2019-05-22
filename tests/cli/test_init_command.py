import shutil
import tempfile
import unittest

from lspace import create_app
from lspace.cli.init_command import init


def get_test_app(test_dir):
    return create_app(app_dir=test_dir)


def get_temp_dir():
    return tempfile.mkdtemp()


class TestInitCommand(unittest.TestCase):

    def setUp(self) -> None:
        self.test_dir = get_temp_dir()
        self.app = get_test_app(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_init_command(self):
        runner = self.app.test_cli_runner()

        # invoke the command directly
        result = runner.invoke(init, [])
        assert result.exit_code == 0
        assert 'written config file to ' in result.output
        assert self.test_dir in result.output
