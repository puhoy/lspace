import click

from lspace.cli.import_command.base_helper import BaseHelper


class Peek(BaseHelper):
    explanation = 'peek in the text'

    @classmethod
    def function(cls, file_type_object, old_choices, *args, **kwargs):
        click.echo_via_pager(file_type_object.get_text())
        return old_choices
