import logging
import os

from shutil import copyfile, move
from slugify import slugify

from lspace.helpers import find_unused_path
from flask import current_app
from lspace.file_types._base import FileTypeBase

logger = logging.getLogger(__name__)


def _copy_to_library(file_type_object, result, move_file):
    # type: (FileTypeBase, dict, bool) -> str
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen result
    :param move_file: move instead of copy
    :return:
    """
    # prepare the fields for path building
    author_slugs = [slugify(author_name) for author_name in result['Authors'] if author_name]

    if not author_slugs:
        author_slugs = ['UNKNOWN-AUTHOR']

    authors = '_'.join(author_slugs)
    title = slugify(result['Title'])

    logger.debug('author slug: %s' % authors)
    logger.debug('title slug: %s' % title)

    path_in_library = find_unused_path(current_app.config['LIBRARY_PATH'],
                                       current_app.config['USER_CONFIG']['file_format'], authors, title,
                                       file_type_object.extension)
    target_path = os.path.join(current_app.config['LIBRARY_PATH'], path_in_library)

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
        # update path before move, or we lose reference
        if file_type_object.path != target_path:
            move(file_type_object.path, target_path)
            file_type_object.path = target_path
        else:
            logger.info('source and target path are the same - skip moving the file')

    return path_in_library
