from lspace.cli.import_command.base_helper import BaseHelper


class SkipBook(BaseHelper):
    explanation = 'skip this book'

    @classmethod
    def function(cls, *args, **kwargs):
        return False
