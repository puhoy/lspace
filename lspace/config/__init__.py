import os
import logging
from ..app import app

user_config = app.config['USER_CONFIG']

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
