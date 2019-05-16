import logging
import os

import isbnlib
import yaml

from .. import CONFIG_FILE
from .. import app_dir

logger = logging.getLogger(__name__)


def get_default_config():
    this_dir = os.path.dirname(os.path.abspath(__file__))
    path_from_here = '../config/'
    with open(os.path.join(this_dir, path_from_here, 'default_conf.yaml'), 'r') as default_config_file:
        default_config = yaml.load(default_config_file, Loader=yaml.SafeLoader)
        default_config['database_path'] = default_config['database_path'].format(
            APP_DIR=app_dir)
    return default_config


def read_config():
    config_path = os.path.join(app_dir, CONFIG_FILE)
    if os.path.isfile(config_path):
        with open(config_path, 'r') as config:
            conf = yaml.load(config, Loader=yaml.SafeLoader)

    else:
        conf = {}

    conf = {**get_default_config(), **conf}
    return conf


def get_metadata_for_isbn(isbn, serice='openl') -> dict:
    try:
        meta = isbnlib.meta(isbn, service='openl', cache='default')
    except (isbnlib.dev._exceptions.NoDataForSelectorError,
            isbnlib._exceptions.NotValidISBNError,
            isbnlib.dev._exceptions.DataNotFoundAtServiceError
            ):
        meta = {}
    return meta


def query_isbn_data(isbn_str) -> dict:
    if isbnlib.is_isbn10(isbn_str):
        isbn_str = isbnlib.to_isbn13(isbn_str)

    meta = get_metadata_for_isbn(isbn_str, 'openl')

    if not meta:
        meta = get_metadata_for_isbn(isbn_str, 'goob')

    if meta:
        return meta
    else:
        return None


def query_google_books(words):
    logger.debug('query google books for %s' % words)
    try:
        results = isbnlib.goom(words)
    except isbnlib.dev._exceptions.NoDataForSelectorError as e:
        results = []
    return results


def query_db(query, books=True, authors=True):
    from ..models import Book, Author
    if not query or (len(query) == 1 and not query[0]):
        results = Book.query.all()
    else:
        results = Book.query.whooshee_search(' '.join(query)).all()
        author_results = Author.query.whooshee_search(' '.join(query)).all()
        for author in author_results:
            for book in author.books:
                results.append(book)
    return results


def find_unused_path(base_path, book_path_format, authors: str, title: str, extension: str) -> str:
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
            path_from_base_path = f'{path_from_base_path}_{count}{extension}'

        target_path = os.path.join(base_path, path_from_base_path)

        if not os.path.exists(target_path):
            return path_from_base_path

        count += 1
    return False
