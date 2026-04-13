from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3*gpkqzm)(7n4gfub4cnw#1vqy!-h6^1*n5$c=sz*p6&jyx9e8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["localhost"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # packages
    'rest_framework',
    'knox',
    'django_filters',
    'corsheaders',
    'django_rest_passwordreset',
    'drf_yasg',

    # apps
    'users',
    'authentication',
    'balances',
    'brands',
    'faqs',
    'favorites',
    'locations',
    'metal_types',
    'products',
    'testimonies',
    'charts',
    'pricing',
    'gallery',
    'sliders',
    'manufacture_fees',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'precious_collectibles.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "precious_collectibles/templates"
            ],
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

WSGI_APPLICATION = 'precious_collectibles.wsgi.application'

AUTH_USER_MODEL = "users.User"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'knox.auth.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 50
}

REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'USER_SERIALIZER': 'users.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': None,
  'AUTO_REFRESH': False,
  'TOKEN_TTL': None
}

# validate domain email
ABSTRACT_API_KEY = ''
ABSTRACT_BASE_URL = f'https://emailvalidation.abstractapi.com/v1/?api_key={ABSTRACT_API_KEY}&'

APP_NAME = 'NAGM ED-DIN'
EXPIRE_VERIFICATION_CODE_MINUTES = 10

# email config
EMAIL_HOST_USER = ''
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'djangodeveloper123@gmail.com'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
EMAIL_CONTACT_US = DEFAULT_FROM_EMAIL
EMAIL_HOST_PASSWORD = ''

# reset password configuration
DJANGO_REST_PASSWORDRESET_TOKEN_CONFIG = {
    "CLASS": "django_rest_passwordreset.tokens.RandomNumberTokenGenerator",
    "OPTIONS": {
        "min_number": 100000,
        "max_number": 999999
    }
}

# cors config
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'POST',
    'PUT',
    'PATCH',
]



# # config celery
# CELERY_BROKER_URL = "redis://localhost:6379"
# CELERY_RESULT_BACKEND = "redis://localhost:6379"


# URL LIVE PRICE
LIVE_PRICE_URL = "https://dahabmasr.com/pub/running/plu/CurrPrice.json"

from decimal import Decimal
# KIRAT_FROM_21
KIRAT_24_FROM_21 = Decimal(999.9 / 875)
KIRAT_18_FROM_21 = Decimal(6 / 7)
import os

log_filename = BASE_DIR / "logs/system.log"

os.makedirs(os.path.dirname(log_filename), exist_ok=True)

# logging configurations
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s  %(module)s %(filename)s %(funcName)s "
                      "%(lineno)d %(message)s"
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': log_filename,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        }
    },
    "loggers": {
        'root': {
            'level': "DEBUG",
            'handlers': ['file'],
            'propagate': True
        },
        'django': {
            "level": "INFO",
            "handlers": ["console", "file"],
            "propagate": True
        },
        'django.request': {
            "level": "INFO",
            "handlers": ['mail_admins', "file"],
            'propagate': False
        },
        'django.server': {
            "level": "INFO",
            "handlers": ['mail_admins', "file"],
            'propagate': False
        }
    },
}




