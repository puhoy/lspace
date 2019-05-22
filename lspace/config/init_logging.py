import logging

from flask import current_app


def init_logging():
    user_config = current_app.config['USER_CONFIG']

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
