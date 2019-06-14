from copy import deepcopy
from typing import Union

import click
import yaml

from lspace.cli.import_command.base_helper import BaseHelper
from lspace.cli.import_command.import_options.peek import Peek
from lspace.file_types import FileTypeBase
from lspace.helpers import preprocess_isbns
from lspace.models import Book


class ManualImport(BaseHelper):
    explanation = 'import manually'

    @classmethod
    def function(cls, file_type_object, old_choices, *args, **kwargs):
        return manual_import(file_type_object, old_choices)


def _prompt_choices(msg):
    choice = False

    while choice not in ['e', 'r']:
        choice = click.prompt(
            click.style(
                msg + ' \n' +
                'e: edit\n' +
                'r: restart with empty form\n' +
                'c: cancel editing\n' +
                'p: ' + Peek.explanation + '\n',
                bold=True),
            type=click.Choice(['e', 'r', 'p', 'c']), default='e')
        return choice


def _get_edit_text(path):
    _edit_dict = dict(
        Title='',
        Authors=['', ],
        ISBN='',
        Publisher='',
        Year='',
        Language='',
    )
    edit_dict = deepcopy(_edit_dict)

    text = '# import {path}\n'.format(path=path)
    text += '# only the title is needed, but you probably want to specify more :)\n\n'
    text += yaml.dump(edit_dict, sort_keys=False)
    return text


def get_edit_result(file_type_object):
    # type: (FileTypeBase) -> Union[dict, bool]
    edit_text = _get_edit_text(file_type_object.path)
    choice = 'e'

    while True:
        if choice == 'e':
            result = click.edit(edit_text, require_save=True)

            if result:
                book_dict = yaml.load(result, Loader=yaml.FullLoader)
                if book_dict['Title']:
                    return book_dict
                else:
                    choice = _prompt_choices('title is needed!')
                    edit_text = result

            else:
                choice = _prompt_choices('no data! did you save?')

        elif choice == 'r':
            edit_text = _get_edit_text(file_type_object.path)
            choice = 'e'

        elif choice == 'p':
            Peek.function(file_type_object, old_choices=[])
            choice = _prompt_choices(click.style('', bold=True))

        elif choice == 'c':
            return False

        else:
            # it shouldnt be possible to get here, but just in case..
            choice = 'e'
            pass


def manual_import(file_type_object, old_choices):
    # type: (FileTypeBase, [Book]) -> [dict]

    result = get_edit_result(file_type_object)
    if not result:
        return old_choices

    isbn = result.get('ISBN')
    if isbn:
        isbns = preprocess_isbns([isbn])
        if len(isbns) == 1:
            isbn = isbns[0]
            result['ISBN-13'] = isbn

    return [Book.from_search_result(result, metadata_source='manually added')]
