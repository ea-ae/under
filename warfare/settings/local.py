# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Logging

LOGGING = {
    'version': 1,
    'formatters': {
        'general': {
            'format': '{levelname}\t{asctime}\t{message}',
            'style': '{'
        }
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # Log SQL queries when DEBUG enabled
            'class': 'logging.StreamHandler',
            'formatter': 'general'
        },
        'userinfo': {  # Valid user actions
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/userlog.log',
            'formatter': 'general'
        },
        'usererrors': {  # When the user does something that we don't expect
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/usererrors.log',
            'formatter': 'general'
        },
        'djangoerrors': {  # Server errors
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/errors.log',
            'formatter': 'general'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['djangoerrors'],
        },
        'warfare': {
            'level': 'INFO',
            'handlers': ['userinfo', 'usererrors', 'console'],
            'propagate': True
        }
    }
}
