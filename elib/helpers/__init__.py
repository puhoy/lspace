import os

import yaml
import logging
import isbnlib

from .. import app_dir
from .. import CONFIG_FILE


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
    with open(config_path, 'r') as config:
        conf = yaml.load(config, Loader=yaml.SafeLoader)

    conf = {**get_default_config(), **conf}

    loglevel = logging._nameToLevel[conf.get('loglevel', 'INFO')]
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=loglevel)

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
