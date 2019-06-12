import logging
import os

import isbnlib
import yaml

logger = logging.getLogger(__name__)


def get_default_config(app_dir):
    default_config = {
        'database_path': 'sqlite:///{APP_DIR}/lspace.db'.format(
            APP_DIR=app_dir),
        'library_path': '~/library',
        'file_format': '{AUTHORS}/{TITLE}',
        'loglevel': 'error'
    }
    return default_config


def read_config(config_path, app_dir):
    if os.path.isfile(config_path):
        with open(config_path, 'r') as config:
            conf = yaml.load(config, Loader=yaml.SafeLoader)

    else:
        conf = {}

    config = get_default_config(app_dir)
    config.update(conf)
    return config


def find_unused_path(base_path, book_path_format, authors, title, extension):
    # type: (str, str, str, str, str) -> str
    """

    :param base_path: 
    :param book_path_format: 
    :param authors: 
    :param title: 
    :param extension: 
    :return: new path relative from base_path  
    """
    # create the path for the book

    count = 0

    while count < 100:
        path_from_base_path = book_path_format.format(
            AUTHORS=authors, TITLE=title)
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


def preprocess_isbns(isbns):
    """

    :param isbns: isbns in different formats
    :return: canonical isbn13s
    """
    canonical_isbns = []
    for isbn in isbns:
        if not isbnlib.notisbn(isbn, level='strict'):
            if isbnlib.is_isbn10(isbn):
                isbn = isbnlib.to_isbn13(isbn)
            isbn = isbnlib.get_canonical_isbn(isbn)
            canonical_isbns.append(isbn)
    canonical_isbns = set(canonical_isbns)
    return list(canonical_isbns)
