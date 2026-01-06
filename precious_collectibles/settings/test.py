from .base import *

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'dbtest.sqlite3',
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
STATICFILES_DIRS = []
MEDIA_ROOT = BASE_DIR / 'media/test'
# configure logging
LOGGING = None
USE_X_FORWARDED_HOST = None

# config celery as a test
CELERY_TASK_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

