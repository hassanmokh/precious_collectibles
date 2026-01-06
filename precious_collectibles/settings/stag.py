from .base import *

ALLOWED_HOSTS = ['80.85.153.112']

ADMINS = (
    ('hassan mokhtar', 'hassan.mokhtar996@gmail.com'),
)

DATABASES['default'] = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'precious_collectibles', 
    'USER': "nagm_addin_3*gpkqzm",
    'PASSWORD': "GPbkGLldX3OPQVhcgpJ5M9LVebJA3fm0q52nXYaN4",
    'HOST': '127.0.0.1', 
    'PORT': '5432',
}

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