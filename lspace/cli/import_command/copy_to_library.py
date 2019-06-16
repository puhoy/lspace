import logging
import os
from shutil import copyfile, move

from flask import current_app

from lspace.models import Book

logger = logging.getLogger(__name__)


def copy_to_library(source_path, book, move_file):
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


def find_unused_path(base_path, book_path_format, source_path, book, extension=None):
    # type: (str, str, str, Book) -> str
    """

    :param base_path: path to the library
    :param book_path_format: template for path in library from user config
    :param book:
    :return: new path relative from base_path
    """
    # create the path for the book

    count = 0
    if not extension:
        _, extension = os.path.splitext(source_path)

    while count < 100:
        path_from_base_path = book_path_format.format(
            AUTHORS=book.author_names_slug,
            TITLE=book.title_slug,
            SHELVE=book.shelve_name_slug,
            YEAR=book.year,
            LANGUAGE=book.language_slug,
            PUBLISHER=book.publisher_slug
        )
        # if, for some reason, the path starts with /, we need to make it relative
        while path_from_base_path.startswith(os.sep):
            logger.debug('trimming path to %s' % path_from_base_path[1:])
            path_from_base_path = path_from_base_path[1:]

        if count == 0:
            path_from_base_path += extension
        else:
            path_from_base_path = '{path_from_base_path}_{count}{extension}'.format(
                path_from_base_path=path_from_base_path,
                count=count, extension=extension)

        target_path = os.path.join(base_path, path_from_base_path)

        if not os.path.exists(target_path):
            return path_from_base_path

        count += 1
    return False