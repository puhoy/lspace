
import logging

from lspace.file_types import FileTypeBase
from lspace.models import Book

logger = logging.getLogger(__name__)

def add_book_to_db(file_type_object, result, path_in_library):
    # type: (FileTypeBase, Book, str) -> Book
    """

    :param file_type_object: wrapper for the file we want to import
    :param result: chosen metadata result
    :param path_in_library: the path after import
    :return:
    """

    result.md5sum=file_type_object.get_md5()
    result.path=path_in_library

    logger.info('adding book %s' % result.to_dict())

    result.save()

    return result
