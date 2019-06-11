
from logging.config import dictConfig

def init_logging(loglevel='info'):
    dictConfig({
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(name)s [%(levelname)s]: %(message)s'
            },
        },
        'handlers': {
            'default': {
                'level': loglevel.upper(),
                'class': 'logging.StreamHandler',
                'formatter': 'default'
            },
        },
        'loggers': {
            '': {
                'handlers': ['default'],
                'level': loglevel.upper(),
                'propagate': True
            },
            'alembic': {
                'handlers': ['default'],
                'level': 'WARNING',
                'propagate': True
            }

            #'sqlalchemy.engine': {
            #    'handlers': ['default'],
            #    'level': loglevel.upper(),
            #    'propagate': False
            #}
        }
    })
