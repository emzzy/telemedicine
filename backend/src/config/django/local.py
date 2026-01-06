from .base import *

DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

ALLOWED_HOSTS += [
        "127.0.0.1",
        "localhost",
        "http://localhost:5173/"
    ]

STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
        'OPTIONS': {
        },
    },

    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    # BASE_DIR / 'frontend' / 'static',
    BASE_DIR / 'static',
]

STATIC_ROOT = BASE_DIR / 'staticfiles' # for prod


MEDIA_URL = '/media/'