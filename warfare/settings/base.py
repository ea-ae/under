import os
from .secret import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config['SECRET_KEY']

ALLOWED_HOSTS = config['ALLOWED_HOSTS']

ASGI_APPLICATION = 'game.routing.application'
WSGI_APPLICATION = 'warfare.wsgi.application'

ROOT_URLCONF = 'warfare.urls'

AUTH_USER_MODEL = 'main.User'

LOGIN_REDIRECT_URL = '../'

# SESSION_COOKIE_AGE = 604800
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# View to redirect to if ratelimited
RATELIMIT_VIEW = 'main.views.ratelimited'


# Channel layers

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [(config['REDIS_IP'], 6379)],
        },
    }
}

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
        'userinfo_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/info.log',
            'formatter': 'general'
        },
        'usererror_file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': 'logs/info.log',
            'formatter': 'general'
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': 'logs/usererror.log',
            'formatter': 'general'
        }
    },
    'loggers': {
        # 'django': {
        #     'handlers': ['console'],
        #     'propagate': True
        # },
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['error_file'],
        },
        'warfare': {
            'level': 'INFO',
            'handlers': ['userinfo_file', 'usererror_file', 'console'],
            'propagate': True
        }
    }
}

# Application definition

INSTALLED_APPS = [
    'game.apps.GameConfig',
    'main.apps.MainConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PASSWORD_HASHERS = [
    'warfare.hashers.BCryptSHA256Custom',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [(os.path.join(BASE_DIR, 'templates'))],  # Global templates
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'warfare',
        'USER': 'warfare',
        'PASSWORD': config['DB_PASSWORD'],
        'HOST': 'localhost',
        'PORT': '5432'
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles/')  # Collected static fields directory
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Global static files
]
