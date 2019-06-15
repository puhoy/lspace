import logging
import os

import isbnlib
import yaml
import typing

if typing.TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


def get_default_config(app_dir):
    default_config = {
        'database_path': 'sqlite:///{APP_DIR}/lspace.db'.format(
            APP_DIR=app_dir),
        'library_path': '~/library',
        'file_format': '{AUTHORS}/{TITLE}',
        'loglevel': 'error',
        'default_shelve': 'misc',
        'default_author': 'no author',
        'default_language': 'no language',
        'default_publisher': 'no publisher'
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
