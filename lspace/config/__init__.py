import os
import logging

from ..helpers import read_config

user_config = read_config()

library_path = os.path.abspath(os.path.expanduser(user_config['library_path']))

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(name)s [%(levelname)s]: %(message)s'
        },
    },
    'handlers': {
        'default': {
            'level': user_config.get('loglevel', 'INFO').upper(),
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': user_config.get('loglevel', 'INFO').upper(),
            'propagate': True
        }
    }
})
