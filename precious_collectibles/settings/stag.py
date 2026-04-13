from .base import *


STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "static"
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'POST',
    'PUT',
    'PATCH',
]

CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)