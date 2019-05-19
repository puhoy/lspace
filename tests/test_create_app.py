import unittest

from lspace import create_app


class TestCreateApp(unittest.TestCase):
    def test_create_app(self):
        """
        basic first test: just check if it breaks when app is created and commands imported

        :return:
        """
        app = create_app()
        from lspace.cli import cli as cli_group
        assert app
