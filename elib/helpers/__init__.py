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
        default_config['database_path'] = default_config['database_path'].format(APP_DIR=app_dir)
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



def query_isbn_data(isbn):
    if isbnlib.is_isbn10(isbn_str):
        isbn_str = isbnlib.to_isbn13(isbn_str)
    try:
        meta = isbnlib.meta(isbn_str, service='openl', cache='default')
    except isbnlib.dev._exceptions.NoDataForSelectorError:
        meta = {}
    if not meta:
        try:
            meta = isbnlib.meta(isbn_str, service='goob', cache='default')
        except isbnlib.dev._exceptions.NoDataForSelectorError:
            meta = {}
    if meta:
        return [meta]
    else:
        return []

