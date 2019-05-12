import logging
import os

from shutil import copyfile, move
from slugify import slugify

from lspace.config import library_path, user_config

logger = logging.getLogger(__name__)


def _copy_to_library(file_type_object, result, move_file) -> str:
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen result
    :param move_file: move instead of copy
    :return:
    """
    # prepare the fields for path building
    author_slugs = [slugify(author_name) for author_name in result['Authors']]
    if not author_slugs:
        author_slugs = ['UNKNOWN AUTHOR']

    AUTHORS = '_'.join(author_slugs)
    TITLE = slugify(result['Title'])

    logger.debug('author slug: %s' % AUTHORS)
    logger.debug('title slug: %s' % TITLE)

    # create the path for the book
    path_found = False
    count = 0
    path_in_library = False
    while not path_found and count < 100:
        path_in_library = user_config['file_format'].format(
            AUTHORS=AUTHORS, TITLE=TITLE)
        # if, for some reason, the path starts with /, we need to make it relative
        while path_in_library.startswith(os.sep):
            logger.debug('trimming path to %s' % path_in_library[1:])
            path_in_library = path_in_library[1:]

        if count == 0:
            path_in_library += file_type_object.extenstion
        else:
            path_in_library = f'{path_in_library}_{count}{file_type_object.extenstion}'

        target_path = os.path.join(library_path, path_in_library)

        if not os.path.exists(target_path):
            path_found = True

        count += 1

    if not path_found:
        logger.error('could not find a path in the library for %s' %
                     file_type_object.path)
        return False

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    logger.debug('importing to %s' % target_path)
    if not move_file:
        copyfile(file_type_object.path, target_path)
    else:
        move(file_type_object.path, target_path)

    return path_in_library
