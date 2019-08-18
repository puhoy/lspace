from copy import deepcopy
from typing import Union

import click
import yaml

from lspace.cli.import_command.base_helper import BaseHelper
from lspace.cli.import_command.import_options.peek import Peek
from lspace.file_types import FileTypeBase
from lspace.helpers import preprocess_isbns
from lspace.models import Book


class FindMoreResults(BaseHelper):
    explanation = 'try to find more based on file'

    @classmethod
    def function(cls, file_type_object, old_choices, *args, **kwargs):

        return next(file_type_object.results)
