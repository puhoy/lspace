import logging
import os
from shutil import copyfile, move

from flask import current_app

from lspace.helpers import find_unused_path
from lspace.models import Book

logger = logging.getLogger(__name__)


def _copy_to_library(source_path, book, move_file):
    # type: (str, Book, bool) -> str
    """

    :param source_path: path to the file we want to import
    :param book: chosen result
    :param move_file: move instead of copy
    :return:
    """
    # prepare the fields for path building

    library_path = current_app.config['USER_CONFIG']['library_path']
    path_in_library = find_unused_path(library_path,
                                       current_app.config['USER_CONFIG']['file_format'],
                                       source_path,
                                       book)
    target_path = os.path.join(library_path, path_in_library)

    if not target_path:
        logger.error('could not find a path in the library for %s' %
                     source_path)
        return False

    if not os.path.isdir(os.path.dirname(target_path)):
        os.makedirs(os.path.dirname(target_path))

    logger.debug('importing to %s' % target_path)
    if not move_file:
        copyfile(source_path, target_path)
    else:
        if source_path != target_path:
            move(source_path, target_path)
        else:
            logger.info('source and target path are the same - skip moving the file')

    return path_in_library
