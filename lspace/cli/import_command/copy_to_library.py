import logging
import os

from shutil import copyfile, move

from lspace.helpers import find_unused_path
from flask import current_app
from lspace.file_types._base import FileTypeBase
from lspace.models import Book

logger = logging.getLogger(__name__)


def _copy_to_library(file_type_object, result, move_file):
    # type: (FileTypeBase, Book, bool) -> str
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen result
    :param move_file: move instead of copy
    :return:
    """
    # prepare the fields for path building

    library_path = current_app.config['USER_CONFIG']['library_path']
    path_in_library = find_unused_path(library_path,
                                       current_app.config['USER_CONFIG']['file_format'],
                                       result.author_names_slug,
                                       result.title_slug,
                                       file_type_object.extension)
    target_path = os.path.join(library_path, path_in_library)

    if not target_path:
        logger.error('could not find a path in the library for %s' %
                     file_type_object.path)
        return False

    if not os.path.isdir(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path))

    logger.debug('importing to %s' % target_path)
    if not move_file:
        copyfile(file_type_object.path, target_path)
    else:
        if file_type_object.path != target_path:
            move(file_type_object.path, target_path)
        else:
            logger.info('source and target path are the same - skip moving the file')
    file_type_object.path = target_path
    return path_in_library
